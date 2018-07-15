#!/bin/bash
set -e
python3 manage.py migrate
python manage.py runserver 0.0.0.0:$PORT