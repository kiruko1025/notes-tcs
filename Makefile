PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
PORT ?= 8000

.PHONY: all html pdf serve deploy clean

all: pdf

html:
	$(PYTHON) scripts/build_site.py

# HTML cleans out/, so finish it before PDF generation even with parallel make.
pdf: html
	$(PYTHON) scripts/build_pdfs.py

serve: all
	$(PYTHON) -m http.server $(PORT) --directory out

# Publish the latest pushed main commit. Normal pushes trigger this automatically.
deploy:
	gh workflow run main.yml --ref main

clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('out', ignore_errors=True); shutil.rmtree('work/pdf', ignore_errors=True)"
