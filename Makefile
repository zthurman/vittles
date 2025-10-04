# Define variables
PY = python
TEST = unittest
VENV = venv
DEVENV_DIR = devenv
DEVENV_BIN = $(DEVENV_DIR)/bin

phony: test devenv format

test:
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/$(PY) -m $(TEST) discover

devenv:
	$(PY) -m venv $(DEVENV_DIR)
	. $(DEVENV_BIN)/activate
	$(DEVENV_BIN)/pip install -r dev-requirements.txt

format:
	. $(DEVENV_DIR)/bin/activate
	$(DEVENV_DIR)/bin/black .
	
