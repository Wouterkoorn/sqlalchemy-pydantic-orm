#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Running tests with coverage and pytest"

coverage run -m pytest tests/

echo "Coverage report"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

coverage report -m

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Reformatting code with black"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

black sqlalchemy_pydantic_orm/ examples/ tests/ setup.py

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Reordering imports with isort"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

isort sqlalchemy_pydantic_orm/ examples/ tests/ setup.py


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Reviewing code type hinting with mypy"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

mypy sqlalchemy_pydantic_orm/ examples/ tests/ setup.py

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Reviewing code style with flake8"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

flake8
