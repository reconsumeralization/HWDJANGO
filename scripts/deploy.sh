#!/bin/bash

# Ensure we're in the project root
cd "$(dirname "$0")/.."

# Check if directories exist before proceeding
if [ ! -d "apps/hwroad" ] || [ ! -d "apps/hwasphalt" ] || [ ! -d "backend" ]; then
    echo "Error: Required directories not found. Please ensure project structure is correct."
    exit 1
fi

# Add package.json to root if it doesn't exist
if [ ! -f "package.json" ]; then
    echo "Error: package.json not found in root directory"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
npm install

# Build frontend apps
echo "Building frontend apps..."
npm run build

# Deploy frontend apps to Vercel
echo "Deploying frontend apps to Vercel..."
cd apps/hwroad
vercel --prod
cd ../hwasphalt
vercel --prod

# Deploy Django backend
echo "Deploying Django backend..."
cd ../../backend
vercel --prod
