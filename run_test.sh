#! /bin/bash
set -euo pipefail

venv/bin/python -m unittest discover -v tests/
