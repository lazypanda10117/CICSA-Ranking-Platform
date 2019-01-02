#!/usr/bin/env bash
python3 ./scripts/setup/setup.py 1
python3 manage.py migrate
python3 ./scripts/setup/setup.py 2
