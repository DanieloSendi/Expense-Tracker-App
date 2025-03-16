#!/usr/bin/env bash
# Exit on error
set -o errexit  

# Installation of packages
pip install -r requirements.txt  

# Converting static files
python manage.py collectstatic --no-input  

# Database migration
python manage.py migrate
