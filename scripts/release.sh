#!/usr/bin/env bash
# Inspired by https://gitlab.cern.ch/pelson/pytimber/-/blob/master/release.sh

set -euo pipefail
IFS=$'\n\t'

NAME=$(python setup.py --name)
VERSION=$(python setup.py --version)


printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Building $NAME v$VERSION with setuptools"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

pip freeze > requirements.txt
python setup.py sdist bdist_wheel

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Releasing $NAME v$VERSION on PyPI with twine"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

twine upload -u wkoorn dist/*

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =
echo "Tagging $NAME v$VERSION on Github"
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' =

git tag -a "v$VERSION"
git push origin "v$VERSION"
