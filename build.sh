#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Install additional dependencies for production
pip install gunicorn psycopg2-binary whitenoise

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
