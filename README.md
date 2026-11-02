# CS Notes

Computer science course notes with searchable documentation, rendered mathematics,
and downloadable collection PDFs.

Live website: <https://kiruko1025.github.io/notes-tcs/>

## Edit notes

Edit the Markdown files in `src/`. Keep lecture filenames numeric for chronological
ordering. Titles, dates, and tags come from YAML frontmatter when present. Empty
files remain visible as unfinished entries. The homepage replaces the old
placeholder `src/index.md`.

The interface is in `web/`; collection names and ordering are configured in
`scripts/build_site.py`. Generated HTML, search data, source downloads, and PDFs
go into `out/`, which is not committed. Files outside this repository are not
required. Citations to such files are labeled as local references.

## Build locally

Create a Python environment and install the renderer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

PDF generation uses Pandoc, XeLaTeX, Noto Serif/Sans, and a supported monospace
font. On Debian/Ubuntu, install them with:

```sh
sudo apt-get install pandoc texlive-xetex texlive-latex-extra texlive-fonts-recommended fonts-noto-core fonts-dejavu-core fontconfig
```

```sh
make all             # Build the website and all five PDF editions
make serve           # Build and preview at http://localhost:8000
make serve PORT=4173  # Use another local port
make html            # HTML only; cleans out/, so use make all before publishing
make clean           # Remove generated output and PDF intermediates
```

Collection PDFs and the complete notebook are in `out/pdfs/`.
`out/documentation.pdf` also serves the complete notebook for compatibility.

## Publish

Commit and push changes to `main`. GitHub Actions builds HTML and PDFs together,
then publishes `out/` to the existing GitHub Pages site. `make deploy` manually
runs that workflow for the latest pushed `main` commit; it does not upload
uncommitted local edits.

The website works under the `/notes-tcs/` project path and at a domain root.
Legacy MkDocs lecture URLs redirect to the corresponding new note, preserving
section bookmarks.

MathJax 3.2.2 is bundled in `web/assets/vendor/`, with its Apache 2.0 license.
