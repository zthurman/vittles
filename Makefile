SHELL:=/bin/bash
UNAME := $(shell uname)

# Python and venv stuff
PY = python
COVERAGE = coverage
TEST = unittest
VENV = venv
VENV_BIN = $(VENV)/bin
REQ_DIR = requirements
REQS = $(REQ_DIR)/requirements.txt
DEVENV_DIR = devenv
DEVENV_BIN = ./$(DEVENV_DIR)/bin
DEVENV_REQS = $(REQ_DIR)/dev-requirements.txt
XDG = xdg-open

# Use this in clean target in case we # try to compile any TeX files without # PyLaTeX
LATEX_ARTIFACTS = *.aux *.pdf *.tex *.log *.fdb_latexmk *.fls *.toc

phony: all env book addrecipe devenv test format clean all

all: env addrecipe book devenv test coverage format

env:
	./ensure-texlive.sh
	$(PY) -m $(VENV) $(VENV)
	. $(VENV_BIN)/activate
	$(VENV_BIN)/pip install -r $(REQS)

addrecipe:
	. $(VENV_BIN)/activate
	$(VENV_BIN)/$(PY) main.py -a

book:
	. $(VENV_BIN)/activate
	$(VENV_BIN)/$(PY) main.py -v
	$(XDG) vittles.pdf

devenv:
	$(PY) -m $(VENV) $(DEVENV_DIR)
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/pip install -r $(DEVENV_REQS)

test:
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/$(COVERAGE) run -m $(TEST) discover

coverage:
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/$(COVERAGE) report

format:
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/black .

clean:
ifneq ($(LATEX_ARTIFACTS),)
	rm -f $(LATEX_ARTIFACTS)
endif
