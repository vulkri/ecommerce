#!/bin/bash

# Run migrations, generate secret key and start server
python manage.py makemigrations
python manage.py migrate
python manage.py djecrety -s -d backend
python -m debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:8000
