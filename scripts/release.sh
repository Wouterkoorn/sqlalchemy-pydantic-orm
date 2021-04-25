#!/usr/bin/env bash
# Inspired by pytimber ;)

set -euo pipefail
IFS=$'\n\t'

NAME=$(python setup.py --name)
VERSION=$(python setup.py --version)

echo "========================================================================"
echo "Building $NAME v$VERSION with setuptools"
echo "========================================================================"

python setup.py sdist bdist_wheel

echo "========================================================================"
echo "Releasing $NAME v$VERSION on PyPI with twine"
echo "========================================================================"

twine upload dist/*

echo "========================================================================"
echo "Tagging $NAME v$VERSION on Github"
echo "========================================================================"

git tag -a "v$VERSION"
git push origin "v$VERSION"
