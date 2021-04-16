#!/usr/bin/env bash
MODULE=${1:-}
coverage run -m unittest discover $MODULE
coverage report -m --omit='venv*'
