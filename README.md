# vittles

This project extends [PyLaTeX](https://github.com/JelteF/PyLaTeX) with [xcookybooky](https://github.com/SvenHarder/xcookybooky) support.

## usage

The usage for this project has been reduced to standard gnumake targets.

### the whole enchilada

    make all

### vittles environment

To add a recipe or make the book, the environment needs to be installed like this:

    make env

### add new recipe

To add a recipe, modify `add_recipe` dict in `main.py` and when done, run:

    make addrecipe

### (re)generate recipe book

To generate the latest `vittles` recipe book, run:

    make book

### development environment

To run tests, check coverage, or format the code. You need to first install
the development environment like this:

    make devenv

### run tests

The tests for the project can be run like this:

    make test

### coverage report

The test coverage for the project can be found like this:

    make coverage

### code formatter

This code is formatted with `black`. To use it:

    make format

### general notes

Sometimes, it can be useful and instructive to try to compile the generated *.tex file manually.
Usually when LaTweaKing out and trying to add all of the cool things.

    make clean

will clean up all of the manual compile build artifacts for you.
 
