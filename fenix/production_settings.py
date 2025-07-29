# production_settings.py - Configuración específica para producción
from .settings import *
import os

# Sobrescribir configuraciones para producción
DEBUG = False

# Configuración más estricta de hosts permitidos en producción
ALLOWED_HOSTS = [
    'fenix-pbad.onrender.com',
    '.onrender.com',  # Para subdominios de Render
]

# Configuración de CORS más específica para producción
CORS_ALLOWED_ORIGINS = [
    # Producción - Dominios específicos de tu frontend
    "https://proyecto2-crud-grupo-5-git-main-johiortizs-projects.vercel.app",
    "https://fenix-crud-app.vercel.app", 
    "https://fenix-crud.onrender.com",
    "https://proyecto2-crud-grupo-5.vercel.app",
    "https://frontend-fenix.vercel.app",
]

# Desactivar CORS_ALLOW_ALL_ORIGINS en producción por seguridad
CORS_ALLOW_ALL_ORIGINS = False

# Configuración de base de datos para producción
# Ya está configurada en settings.py con dj_database_url

# Configuración de archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de logging más detallada para producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/tmp/django_errors.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'fenix': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Configuración de seguridad adicional para producción
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
