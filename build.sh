#!/usr/bin/env bash

npm install --prefix theme/static_src


python manage.py tailwind build


python manage.py migrate


python manage.py collectstatic --noinput
