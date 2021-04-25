#!/usr/bin/env bash
# Inspired by pytimber ;)

set -euo pipefail
IFS=$'\n\t'

NAME=$(python setup.py --name)
VERSION=$(python setup.py --version)

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Building $NAME v$VERSION with setuptools"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

python setup.py sdist bdist_wheel

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Releasing $NAME v$VERSION on PyPI with twine"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

twine upload dist/*

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Tagging $NAME v$VERSION on Github"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

git tag -a "v$VERSION"
git push origin "v$VERSION"
