# Define variables
PY = python
TEST = unittest
VENV = venv
DEVENV_DIR = devenv

phony: test devenv

test:
	$(PY) -m $(TEST) discover

devenv:
	$(PY) -m venv $(DEVENV_DIR)
	. $(DEVENV_DIR)/bin/activate
	$(DEVENV_DIR)/bin/pip install -r dev-requirements.txt
