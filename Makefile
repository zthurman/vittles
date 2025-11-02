SHELL:=/bin/bash

# Python and venv stuff
PY = python
COVERAGE = coverage
TEST = unittest
VENV = venv
VENV_BIN = $(VENV)/bin
REQ_DIR = requirements
REQS = $(REQ_DIR)/requirements.txt
DEVENV_DIR = devenv
DEVENV_BIN = $(DEVENV_DIR)/bin
DEVENV_REQS = $(REQ_DIR)/dev-requirements.txt
XDG = xdg-open

# Use this in clean target in case we
# try to compile any TeX files without
# PyLaTeX
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
ifeq ($(OS),Windows_NT)
	call $(DEVENV_DIR)\Scripts\activate.bat
	$(DEVENV_DIR)\Scripts\pip.exe install -r $(DEVENV_REQS)
else
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/pip install -r $(DEVENV_REQS)
endif

test:
ifeq ($(OS),Windows_NT)
	call $(DEVENV_DIR)\Scripts\activate.bat
	$(DEVENV_DIR)\Scripts\coverage.exe run -m $(TEST) discover
else
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/$(COVERAGE) run -m $(TEST) discover
endif

coverage:
ifeq ($(OS),Windows_NT)
	call $(DEVENV_DIR)\Scripts\activate.bat
	$(DEVENV_DIR)\Scripts\coverage.exe report
else
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/$(COVERAGE) report
endif

format:
ifeq ($(OS),Windows_NT)
	call $(DEVENV_DIR)\Scripts\activate.bat
	$(DEVENV_DIR)\Scripts\black.exe .
else
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/black .
endif

clean:
ifneq ($(LATEX_ARTIFACTS),)
	rm -f $(LATEX_ARTIFACTS)
endif
