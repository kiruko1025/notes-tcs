# ---- paths ----
SRC_DIR := src
OUT_DIR := out
TOC     := toc.txt
PDF     := $(OUT_DIR)/documentation.pdf


# ---- commands (override if you need) ----
MKDOCS  := mkdocs
PANDOC  := pandoc
PDFENG  ?= xelatex

# ---- phony ----
.PHONY: all html pdf serve clean deploy

# Build everything
all: html pdf

# MkDocs HTML -> out/
html:
	$(MKDOCS) build --clean

# Pandoc+LaTeX -> out/documentation.pdf
pdf: $(TOC) | $(OUT_DIR)
	$(PANDOC) $$(cat $(TOC)) \
	  --from markdown \
	  --pdf-engine=$(PDFENG) \
	  --toc --number-sections \
	  -V geometry:margin=1in \
	  -V fontsize=11pt \
	  -o $(PDF)

# Local preview for HTML
serve:
	$(MKDOCS) serve

# Publish HTML (and the PDF that sits in out/) to gh-pages
deploy: all
	$(MKDOCS) gh-deploy --force

$(OUT_DIR):
	mkdir -p $(OUT_DIR)

clean:
	rm -rf $(OUT_DIR)
