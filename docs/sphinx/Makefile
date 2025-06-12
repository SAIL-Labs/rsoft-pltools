# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR    = .
BUILDDIR     = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom targets for API documentation generation
apidoc:
	sphinx-apidoc -o . ../../src/rsoft_cad --force --module-first

clean-apidoc:
	rm -f rsoft_cad*.rst modules.rst

rebuild: clean-apidoc apidoc html

# GitHub Pages target
gh-pages: clean-apidoc apidoc
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "../_build" $(SPHINXOPTS) $(O)
	@echo "Documentation built for GitHub Pages"