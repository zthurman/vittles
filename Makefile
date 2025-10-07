SHELL:=/bin/bash

# Python and venv stuff
PY = python
TEST = unittest
VENV = venv
VENV_BIN = $(VENV)/bin
REQ_DIR = requirements
REQS = $(REQ_DIR)/requirements.txt
DEVENV_DIR = devenv
DEVENV_BIN = $(DEVENV_DIR)/bin
DEVENV_REQS = $(REQ_DIR)/dev-requirements.txt

# Use this in clean target in case we
# try to compile any TeX files without
# PyLaTeX
LATEX_ARTIFACTS = *.aux *.pdf *.tex *.log

phony: book addrecipe env test devenv format clean

book:
	. $(VENV_BIN)/activate
	$(VENV_BIN)/$(PY) main.py -v

addrecipe:
	. $(VENV_BIN)/activate
	$(VENV_BIN)/$(PY) main.py -a

env:
	./ensure-texlive.sh
	$(PY) -m $(VENV) $(VENV)
	. $(VENV_BIN)/activate
	$(VENV_BIN)/pip install -r $(REQS)

test:
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/$(PY) -m $(TEST) discover

devenv:
	$(PY) -m $(VENV) $(DEVENV_DIR)
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/pip install -r $(DEVENV_REQS)

format:
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/black .

clean:
ifneq ($(LATEX_ARTIFACTS),)
	rm -f $(LATEX_ARTIFACTS)
endif
