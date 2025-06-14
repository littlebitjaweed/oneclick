#!/usr/bin/env bash

# Exit immediately on error
set -o errexit

# Install Node.js (required for django-tailwind)
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Install Tailwind CSS dependencies
npm install --prefix theme/static_src

# Build Tailwind CSS
python manage.py tailwind build

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
