#!/usr/bin/env bash

# Install Tailwind dependencies
cd mytheme  # Replace with your Tailwind app name
npm install
npm run build
cd ..

# Collect static files
python manage.py collectstatic --noinput
