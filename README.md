# vittles

This project extends [PyLaTeX](https://github.com/JelteF/PyLaTeX) with [xcookybooky](https://github.com/SvenHarder/xcookybooky) support.

## usage

To add a recipe, modify `add_recipe` dict in `main.py` and when done, run:

    `python main.py -a`

To generate the latest `vittles` recipe book, run:

    `python main.py -v`

## tests

The tests for the project can be run with a make target like this:

- `make test`

## formatter

This code is formatted with `black`. To use it:

- `make devenv` (creates a local venv for you called `devenv`)

- `make format`
 
