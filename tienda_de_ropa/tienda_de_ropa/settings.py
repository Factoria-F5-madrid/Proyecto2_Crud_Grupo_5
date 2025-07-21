from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    
    # Apps
    'categoría',
    'cliente',
    'compra',
    'prenda',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tienda_de_ropa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda_de_ropa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql', 
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='3306'), 
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1, # La versión de la configuración del logging
    'disable_existing_loggers': False, # No deshabilitar los loggers existentes (ej. los de Django)
    'formatters': { # Define cómo se formatearán los mensajes de log
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': { # Define dónde se enviarán los mensajes de log
        'console': { # Un handler que imprime en la consola
            'level': 'INFO', # Nivel mínimo de mensajes a manejar (INFO, WARNING, ERROR, DEBUG)
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        # Opcional: Para guardar logs en un archivo
        # 'file': {
        #     'level': 'WARNING', # Guardará warnings y errores
        #     'class': 'logging.FileHandler',
        #     'filename': 'logs/django_warnings.log', # Ruta donde se guardará el archivo de log
        #     'formatter': 'verbose',
        # },
    },
    'loggers': { # Define los "loggers" que usarán los handlers
        'django': { # El logger de Django
            'handlers': ['console'], # Envía los logs de Django a la consola
            'level': 'INFO', # Muestra INFO, WARNING, ERROR para logs de Django
            'propagate': True, # Permite que los logs se propaguen a loggers superiores
        },
        '': { # El logger "root" (captura mensajes de log de toda la aplicación no manejados por otros loggers)
            'handlers': ['console'],
            'level': 'INFO', # Nivel por defecto para tus propias aplicaciones
            'propagate': False,
        },
        # Ejemplo de logger para una aplicación específica (compra)
        'compra': {
            'handlers': ['console'], # Envía los logs de la app 'compra' a la consola
            'level': 'DEBUG', # Puedes ponerlo en DEBUG para ver más detalles durante el desarrollo
            'propagate': False, # No propagar para evitar duplicidad si el root logger también lo maneja
        },
    },
}