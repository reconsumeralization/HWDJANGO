#!/bin/bash

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Create necessary directories if they don't exist
mkdir -p apps/hwroad apps/hwasphalt backend

# Move Django files to backend if they're in the root
if [ -f "manage.py" ]; then
    mv manage.py backend/
    mv crm backend/
    mv web_front backend/
    mv templates backend/
    mv static backend/
    mv requirements.txt backend/
fi

# Install dependencies
echo "Installing dependencies..."
npm install

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
python -m venv .venv
source .venv/bin/activate || .\.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Start development servers
echo "Starting development servers..."
cd ..
npm run dev:all
