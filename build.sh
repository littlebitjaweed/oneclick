#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install Node.js without apt (Render-safe)
curl -L https://raw.githubusercontent.com/tj/n/master/bin/n -o n
bash n lts
export PATH="$HOME/n/bin:$PATH"

# Install Tailwind dependencies
npm install --prefix theme/static_src

# Build Tailwind CSS
python manage.py tailwind build

# Run Django setup
python manage.py migrate
python manage.py collectstatic --noinput
