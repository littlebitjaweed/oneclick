#!/usr/bin/env bash
# Exit on error
set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
