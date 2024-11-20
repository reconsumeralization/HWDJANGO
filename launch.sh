#!/bin/bash

# Create and activate virtual environment
python -m venv .venv
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate  # Windows
else
    source .venv/bin/activate  # Unix
fi

# Install requirements
pip install -r requirements.txt

# Create .env file from template if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from template. Please update with your settings."
fi

# Create database
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None"

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
