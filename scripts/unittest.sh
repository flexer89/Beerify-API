#!/bin/bash

python3 -m pip install --no-cache-dir --upgrade pip
python3 pip install --no-cache-dir -r requirements.txt

python3 -m pytest tests/
find . -name "*.py" | xargs mypy
