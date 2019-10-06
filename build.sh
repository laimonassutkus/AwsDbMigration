#!/usr/bin/env bash

rm -rf *.egg-info build dist

set -e

python3 setup.py bdist_wheel sdist

while getopts 'ic' flag; do
  case "${flag}" in
    i) python3 -m pip install . ;;
    c) rm -rf *.egg-info build dist ;;
    *) echo 'Unexpected flag.'
       exit 1 ;;
  esac
done
