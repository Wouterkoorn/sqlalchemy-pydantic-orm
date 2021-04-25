#!/usr/bin/env bash

echo "========================================================================"
echo "Running tests with coverage and pytest"

coverage run -m pytest tests/

echo "Coverage report"
echo "========================================================================"

coverage report -m

echo "========================================================================"
echo "Reviewing code with flake8"
echo "========================================================================"

flake8

echo "========================================================================"
echo "Reformatting code with black"
echo "========================================================================"

black sqlalchemy_pydantic_orm/ examples/ tests/ setup.py

echo "========================================================================"
echo "Reordering imports with isort"
echo "========================================================================"

isort sqlalchemy_pydantic_orm/ examples/ tests/ setup.py
