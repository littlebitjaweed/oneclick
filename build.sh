#!/usr/bin/env bash

# Stop if anything fails
set -o errexit

# Install Tailwind dependencies and build CSS
cd theme/static_src
npm install
npm run build
cd ../../

# Collect static files
python manage.py collectstatic --noinput

# Apply DB migrations
python manage.py migrate
