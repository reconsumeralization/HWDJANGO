#!/bin/bash

# Create virtual environment
python -m venv .venv

# Activate virtual environment
if [ -f ".venv/Scripts/activate" ]; then
    # Windows
    source .venv/Scripts/activate
else
    # Unix/Linux
    source .venv/bin/activate
fi

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Create .env file from template if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please update with your settings."
fi

# Apply migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
"

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver 
