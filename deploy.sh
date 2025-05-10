#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install production dependencies
echo "Installing production dependencies..."
pip install gunicorn psycopg2-binary whitenoise

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate

echo "Deployment preparation complete!"
echo "You can now deploy to Render by pushing your code to your Git repository."
echo "Make sure to set up the required environment variables in the Render dashboard."
