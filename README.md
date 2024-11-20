# Django Sealing CRM

A comprehensive CRM system for Robert Stanley Sealing and Paving, built with Django 4.2.

## Features

- Customer Management
- Property & Job Tracking
- Quote Generation
- Invoice Management
- Lead Management
- User Authentication
- File Upload Support
- Reporting System

## Tech Stack

- Django 4.2
- PostgreSQL
- Bootstrap 5
- Django Crispy Forms
- Django Environ

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create .env file with required environment variables
6. Run migrations: `python manage.py migrate`
7. Create superuser: `python manage.py createsuperuser`
8. Run server: `python manage.py runserver`

## Environment Variables
