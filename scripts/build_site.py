#!/usr/bin/env python3
"""Render the preserved Markdown collection into the searchable site catalog."""
import hashlib, json, re, shutil
from pathlib import Path
from html import escape, unescape
import markdown, yaml

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = [
    dict(id='cse574', folder='CSE574', title='CSE574', subtitle='Computational complexity', description='From computation and NP-completeness to hierarchies, oracles, and space complexity.', symbol='P', color='blue'),
    dict(id='cse590', folder='CSE590', title='CSE590', subtitle='Programming language theory', description='Lambda calculus, evaluation strategies, and the semantics of programming languages.', symbol='λ', color='purple'),
    dict(id='algorithms', folder='Algorithms', title='Algorithms', subtitle='Problem-solving techniques', description='Notes on divide and conquer, dynamic programming, and the greedy method.', symbol='↳', color='green'),
    dict(id='mathematical-background', folder='Mathematical Background', title='Mathematical Background', subtitle='Foundations & proof writing', description='A place for the mathematical foundations behind the courses.', symbol='∀', color='orange'),
]

# Old lecture links lead to the corresponding topic after the reorganization.
LEGACY_TOPICS = {
    'cse574': {
        2: '01-computation-and-turing-machines', 3: '03-np-completeness',
        4: '03-np-completeness', 5: '04-hierarchy-theorems',
        6: '06-oracles-and-relativization', 7: '07-polynomial-hierarchy',
        8: '07-polynomial-hierarchy', 9: '08-space-complexity',
        10: '10-logspace-and-nl', 11: '11-time-space-tradeoffs',
        12: '12-circuits-and-advice',
    },
    'cse590': {
        2: '02-lambda-calculus', 3: '02-lambda-calculus',
        4: '03-reduction-and-evaluation', 5: '05-recursion-and-fixed-points',
        6: '06-induction-and-proof-rules', 7: '07-imp-operational-semantics',
        8: '07-imp-operational-semantics', 9: '07-imp-operational-semantics',
        10: '08-imp-denotational-semantics', 11: '09-types-and-type-soundness',
        12: '09-types-and-type-soundness',
    },
}

def natural(path):
    return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', path.name)]

def strip_tags(value):
    return unescape(re.sub('<[^>]+>', ' ', value))

notes = []
for collection in COLLECTIONS:
    files = sorted((ROOT/'src'/collection['folder']).glob('*.md'), key=natural)
    for file in files:
        source = file.read_text()
        body, meta = source, {}
        if source.startswith('---\n'):
            parts = source.split('---', 2)
            if len(parts) == 3:
                meta = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
        heading = re.search(r'^# (.+)', body, re.M)
        fallback = re.sub(r'^\d+-', '', file.stem).replace('-', ' ').title()
        title = str(meta.get('title') or (heading.group(1) if heading else ('Lecture '+file.stem if file.stem.isdigit() else fallback)))
        if collection['id'] == 'algorithms' and file.stem.startswith('1-'):
            title = 'Divide and Conquer'
        note_id = collection['id']+'-'+file.stem
        words = len(body.split())
        state = 'empty' if not body else ('stub' if body.strip() == '# Intro\n\nexample' else 'note')
        md = markdown.Markdown(extensions=['extra', 'toc', 'admonition', 'pymdownx.superfences', 'pymdownx.arithmatex'], extension_configs={'pymdownx.arithmatex': {'generic': True}, 'toc': {'separator': '_'}})
        # Source notes sometimes put display delimiters directly beside prose.
        # Separate those blocks before Markdown can interpret their contents.
        render_body = re.sub(r'(?<=\S)\n(?=1\. )', '\n\n', body)
        render_body = re.sub(r'^\s*\$\$\s*$', '\n\n$$\n\n', render_body, flags=re.M)
        # Keep delimiter-adjacent math lines inside one block (no internal blank lines).
        render_body = re.sub(r'\$\$\s*\n(.*?)\n\s*\$\$', lambda m:'$$\n'+m.group(1).strip()+'\n$$', render_body, flags=re.S)
        html = md.convert(render_body)
        # The page header displays the first H1, preserving later section headings.
        html = re.sub(r'^<h1[^>]*>.*?</h1>\s*', '', html, count=1, flags=re.S)
        plain = re.sub(r'\s+', ' ', strip_tags(html)).strip()
        excerpt_html = re.sub(r'<(span|div) class="arithmatex">.*?</\1>', ' ', html, flags=re.S)
        excerpt = re.sub(r'\s+', ' ', strip_tags(excerpt_html)).strip()
        date = str(meta['date']) if meta.get('date') else None
        path = str(file.relative_to(ROOT/'src'))
        notes.append(dict(id=note_id, collection=collection['id'], path=path, title=title, lecture=int(file.stem) if file.stem.isdigit() else None, html=html, text=plain, excerpt=excerpt, headings=md.toc_tokens, words=words, minutes=max(1, round(words/180)), date=date, tags=meta.get('tags') or [], state=state))

aliases = {f'{course}-{lecture}': f'{course}-{topic}'
           for course, topics in LEGACY_TOPICS.items() for lecture, topic in topics.items()}
note_lookup = {note['id']: note for note in notes}
assert all(target in note_lookup for target in aliases.values()), 'Legacy link target missing'

# Resolve existing Markdown links against their actual source location.
lookup={n['path']:n['id'] for n in notes}
import posixpath
from urllib.parse import unquote
for note in notes:
    def link(match):
        target = unquote(match.group(1))
        file, _, anchor = target.partition('#')
        if not file.endswith('.md'):
            if target.startswith('#'):
                return 'href="#/note/'+note['id']+'?section='+target[1:]+'"'
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(note['path']), file))
        if resolved in lookup:
            return 'href="#/note/'+lookup[resolved]+(('?section='+anchor) if anchor else '')+'"'
        return match.group(0)
    note['html'] = re.sub(r'<a href="(?:/home/|file:)[^"]*">(.*?)</a>', r'<span>\1 (local reference)</span>', note['html'])
    note['html'] = re.sub(r'href="([^"]+)"', link, note['html'])

for collection in COLLECTIONS:
    group = [n for n in notes if n['collection']==collection['id']]
    collection['count'] = len(group)
    collection['populated'] = sum(n['state']!='empty' for n in group)
    collection['pdf'] = 'pdfs/'+collection['id']+'.pdf'

# Validate the catalog before replacing generated output.
output = ROOT / 'out'
if output.exists():
    shutil.rmtree(output)
shutil.copytree(ROOT / 'web', output)
# A new stylesheet URL prevents browsers from reusing an older layout after deploys.
stylesheet_version = hashlib.sha256((output/'assets/style.css').read_bytes()).hexdigest()[:12]
index = output/'index.html'
index.write_text(index.read_text().replace('href="assets/style.css"', f'href="assets/style.css?v={stylesheet_version}"'), encoding='utf-8')
script_version = hashlib.sha256((output/'assets/app.js').read_bytes()).hexdigest()[:12]
index.write_text(index.read_text().replace('src="assets/app.js"', f'src="assets/app.js?v={script_version}"'), encoding='utf-8')
(output/'assets/catalog.json').write_text(json.dumps(dict(collections=COLLECTIONS, notes=notes, aliases=aliases), ensure_ascii=False, default=str), encoding='utf-8')
for file in (ROOT/'src').rglob('*.md'):
    target = output/'source'/file.relative_to(ROOT/'src')
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, target)

# Keep old MkDocs directory URLs and section bookmarks working.
redirects = [(Path(note['path']).with_suffix(''), note) for note in notes]
for collection in COLLECTIONS:
    for lecture, topic in LEGACY_TOPICS.get(collection['id'], {}).items():
        redirects.append((Path(collection['folder'])/str(lecture), note_lookup[collection['id']+'-'+topic]))
for legacy, note in redirects:
    directory = output/legacy
    directory.mkdir(parents=True, exist_ok=True)
    root = '../' * len(legacy.parts)
    route = '/note/' + note['id']
    fallback = root + '#' + route
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(note['title'])} — CS Notes</title>
<script>
const destination = new URL({json.dumps(root)}, location.href);
const section = location.hash.slice(1);
destination.hash = {json.dumps(route)} + (section ? '?section=' + section : '');
location.replace(destination.href);
</script></head><body><a href="{escape(fallback, quote=True)}">Open {escape(note['title'])}</a></body></html>
'''
    (directory/'index.html').write_text(page, encoding='utf-8')
(output/'.nojekyll').touch()
print(f'Built {len(notes)} entries, {len(COLLECTIONS)} collections, and {len(redirects)} legacy redirects in out/.')
