#!/bin/bash

python -m pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

python -m pytest tests/
find . -name "*.py" | xargs mypy
