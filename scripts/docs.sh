#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Generating HTML docs with pdoc3"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

pdoc --html --force -o ./docs ./sqlalchemy_pydantic_orm/
mv ./docs/sqlalchemy_pydantic_orm/* ./docs
rm -rf ./docs/sqlalchemy_pydantic_orm
