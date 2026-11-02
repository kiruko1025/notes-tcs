#!/usr/bin/env python3
"""Build faithful, typeset PDF editions of the existing Markdown notes.

Requires pandoc, xelatex, fontconfig, and PyYAML. Source Markdown is never modified.
Ubuntu packages: pandoc texlive-xetex texlive-latex-extra
texlive-fonts-recommended fonts-noto-core fonts-dejavu-core fontconfig.
Install poppler-utils to render and inspect generated PDFs.
"""
import argparse
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / 'src'
SCRATCH = ROOT / 'work' / 'pdf'
GROUPS = [
    ('cse574', 'CSE574', 'Computational Complexity'),
    ('cse590', 'CSE590', 'Programming Languages'),
    ('algorithms', 'Algorithms', 'Algorithms'),
    ('mathematical-background', 'Mathematical Background', 'Mathematical Background'),
]

HEADER = r'''
\usepackage{amsmath,amssymb}
\usepackage{fancyhdr}
\usepackage{etoolbox}
\usepackage{newunicodechar}
\providecommand{\partialto}{\rightharpoonup}
\newunicodechar{→}{\ensuremath{\to}}
\newunicodechar{⇔}{\ensuremath{\iff}}
\newunicodechar{↔}{\ensuremath{\leftrightarrow}}
\newunicodechar{≠}{\ensuremath{\ne}}
\newunicodechar{≤}{\ensuremath{\le}}
\newunicodechar{・}{\ensuremath{\cdot}}
\newunicodechar{×}{\ensuremath{\times}}
\definecolor{ink}{HTML}{18302D}
\definecolor{accent}{HTML}{25675D}
\AtBeginDocument{\hypersetup{linkcolor=accent,urlcolor=accent}}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\sffamily\color{accent} COMPUTER SCIENCE / NOTES}
\fancyfoot[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.3pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\headheight}{15pt}
\setlength{\emergencystretch}{3em}
\setlength{\parskip}{5pt plus 1pt}
\AtBeginEnvironment{longtable}{\footnotesize}
\AtBeginDocument{\color{ink}}
\widowpenalty=10000
\clubpenalty=10000
'''


def read_note(path):
    text = path.read_text(encoding='utf-8')
    metadata = {}
    if text.startswith('---\n'):
        _, front, text = text.split('---', 2)
        metadata = yaml.safe_load(front) or {}
    text = text.strip()
    text = text.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', ' - ')
    metadata['title'] = str(metadata.get('title', '')).replace('\u2013', '-').replace('\u2014', ' - ')
    return metadata, text


def title_for(path, metadata, text):
    title = metadata.get('title')
    if path.parent.name.startswith('CSE'):
        n = path.stem
        if title:
            title = re.sub(r'^(?:Lecture\s*)?\d+:\s*', '', title)
            return f'Lecture {n}: {title}'
        return f'Lecture {n}'
    if path.stem == '1-divide-and-conquer':
        return 'Divide and Conquer'
    if title:
        return title
    h = re.search(r'^#\s+(.+)', text, re.M)
    return h.group(1) if h else path.stem.replace('-', ' ').title()


def heading_slug(title):
    """Stable anchors also accept MkDocs' underscore-separated fragments."""
    title = re.sub(r'\{#[^}]+\}\s*$', '', title)
    title = re.sub(r'[^\w\s-]', '', title.lower())
    return re.sub(r'[\s_-]+', '-', title).strip('-')


def note_id(path):
    return heading_slug(path.parent.name) + '-' + path.stem


def rewrite_links(text, path, source, included_notes):
    """Keep in-book links internal and label unavailable local references."""
    def replace(match):
        label, raw_target = match.group(1), match.group(2)
        target = raw_target[1:-1] if raw_target.startswith('<') else raw_target
        parsed = urlsplit(target)
        if parsed.scheme and parsed.scheme != 'file':
            return match.group(0)
        local_path = unquote(parsed.path)
        if not local_path and parsed.fragment:
            return f'[{label}](#{note_id(path)}-{heading_slug(unquote(parsed.fragment))})'
        # Other bracket/parenthesis combinations may be mathematical notation.
        if not (local_path.endswith('.md') or local_path.startswith('/') or parsed.scheme == 'file'):
            return match.group(0)
        resolved = (path.parent / local_path).resolve()
        if local_path.endswith('.md') and resolved in included_notes:
            destination = note_id(resolved)
            if parsed.fragment:
                destination += '-' + heading_slug(unquote(parsed.fragment))
            return f'[{label}](#{destination})'
        # A PDF cannot depend on another machine's filesystem. Preserve the
        # citation label, without embedding an inaccessible file URI or path.
        if resolved.is_relative_to(source.resolve()):
            return f'{label} (source reference)'
        return f'{label} (local reference)'

    return re.sub(r'\[([^\]\n]+)\]\((<[^>\n]+>|[^)\n]+)\)', replace, text)


def section_headers(text, path, all_notes):
    lines, inside_fence, extra_level = [], False, 0
    seen = {}
    for line in text.splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            inside_fence = not inside_fence
        match = re.match(r'^(#{1,6})\s+(.+)', line) if not inside_fence else None
        if match:
            original_level, title = len(match.group(1)), match.group(2)
            # Subsequent top-level headings become sections of this note.
            if original_level == 1:
                extra_level = 1
            level = min(6, max(2, original_level + extra_level) + int(all_notes))
            slug = heading_slug(title)
            seen[slug] = seen.get(slug, 0) + 1
            suffix = '' if seen[slug] == 1 else '-' + str(seen[slug])
            line = '#' * level + ' ' + title + ' {#' + note_id(path) + '-' + slug + suffix + '}'
        lines.append(line)
    return '\n'.join(lines)


def note_block(path, source, included_notes, all_notes=False):
    metadata, text = read_note(path)
    title = title_for(path, metadata, text)
    ident = note_id(path)
    level = 2 if all_notes else 1
    # A single canonical chapter title, with all original text preserved below it.
    first = re.match(r'^#\s+(.+)\n?', text)
    if first and (first.group(1) == title or path.parent.name.startswith('CSE') or path.stem == '2-dynamic-programming'):
        text = text[first.end():].lstrip()
    text = section_headers(text, path, all_notes)
    text = rewrite_links(text, path, source, included_notes)
    date = metadata.get('date')
    meta_line = f'*{date}*\n\n' if date else ''
    return ('\\clearpage\n\n' + '#' * level + ' ' + title + ' {#' + ident + '}\n\n'
            + meta_line + (text if text else '*No content yet.*') + '\n\n')


def collect(source, group):
    return sorted((source / group).glob('*.md'), key=lambda p: (0, int(p.stem)) if p.stem.isdigit() else (1, p.name))


def choose_mono_font():
    """Use the existing local font or Ubuntu's packaged DejaVu fallback."""
    for family in ('JetBrains Mono', 'DejaVu Sans Mono', 'Noto Sans Mono'):
        result = subprocess.run(['fc-match', '-f', '%{family}', family], capture_output=True, text=True, check=True)
        if family in result.stdout.split(','):
            return family
    raise RuntimeError('Install fonts-dejavu-core or provide JetBrains Mono or Noto Sans Mono.')


def build_one(source, slug, groups, output, scratch, mono_font):
    is_all = slug == 'all-notes'
    if is_all:
        title, subtitle = 'Computer Science Notes', 'Complete collection'
    else:
        _, name, description = groups[0]
        title, subtitle = name, description if name != description else 'Course notes'
    chunks = []
    included_notes = {p.resolve() for _, name, _ in groups for p in collect(source, name)}
    for _, name, _ in groups:
        if is_all:
            chunks.append('\\clearpage\n\n# ' + name + '\n\n')
        chunks.extend(note_block(p, source, included_notes, is_all) for p in collect(source, name))
    markdown = scratch / (slug + '.md')
    markdown.write_text('\n'.join(chunks), encoding='utf-8')
    header = scratch / 'header.tex'
    header.write_text(HEADER, encoding='utf-8')
    tex = scratch / (slug + '.tex')
    cmd = ['pandoc', str(markdown), '--from=markdown+tex_math_dollars+raw_tex', '--standalone', '--toc', '--toc-depth=2',
           '-V', 'documentclass=article', '-V', 'papersize=letter', '-V', 'geometry=margin=0.78in',
           '-V', 'fontsize=10pt', '-V', 'mainfont=Noto Serif', '-V', 'sansfont=Noto Sans',
           '-V', 'monofont=' + mono_font, '-V', 'monofontoptions=Scale=0.82',
           '-V', 'linestretch=1.08', '-V', 'colorlinks=true', '-V', 'linkcolor=teal',
           '-M', 'title=' + title, '-M', 'subtitle=' + subtitle, '-M', 'date=',
           '--include-in-header=' + str(header), '-o', str(tex)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    (scratch / (slug + '-pandoc.log')).write_text(r.stdout + r.stderr)
    r.check_returncode()
    for attempt in range(3):
        r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory=' + str(scratch), str(tex)], capture_output=True, text=True)
        (scratch / (slug + '-compile.log')).write_text(r.stdout + r.stderr)
        if r.returncode:
            print(r.stdout[-5000:])
            r.check_returncode()
    target = output / (slug + '.pdf')
    target.write_bytes((scratch / (slug + '.pdf')).read_bytes())
    print(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--output', type=Path, default=ROOT / 'out' / 'pdfs')
    parser.add_argument('--scratch', type=Path, default=SCRATCH)
    parser.add_argument('--only', choices=[x[0] for x in GROUPS] + ['all-notes'])
    parser.add_argument('--mono-font', help='Override the automatically selected monospace font.')
    args = parser.parse_args()
    args.source = args.source.resolve()
    args.output = args.output.resolve()
    args.scratch = args.scratch.resolve()
    if not args.source.is_dir():
        parser.error(f'Notes directory does not exist: {args.source}')
    mono_font = args.mono_font or choose_mono_font()
    args.output.mkdir(parents=True, exist_ok=True)
    args.scratch.mkdir(parents=True, exist_ok=True)
    for group in GROUPS:
        if not args.only or args.only == group[0]:
            build_one(args.source, group[0], [group], args.output, args.scratch, mono_font)
    if not args.only or args.only == 'all-notes':
        build_one(args.source, 'all-notes', GROUPS, args.output, args.scratch, mono_font)
        compatibility_pdf = args.output.parent / 'documentation.pdf'
        compatibility_pdf.write_bytes((args.output / 'all-notes.pdf').read_bytes())
        print(compatibility_pdf)


if __name__ == '__main__':
    main()
