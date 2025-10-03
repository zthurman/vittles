# Define variables
PY = python
TEST = unittest

phony: test

test:
	$(PY) -m $(TEST) discover
