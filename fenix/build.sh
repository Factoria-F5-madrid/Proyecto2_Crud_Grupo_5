!/usr/bin/env bash

# Exit on error
set -o errexit

# Instala dependencias si hace falta (Render ya lo hace si usas requirements.txt)
pip install -r requirements.txt

# Ejecuta migraciones y recolecta estáticos
python manage.py migrate
python manage.py collectstatic --noinput
