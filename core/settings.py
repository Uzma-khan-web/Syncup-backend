import os
import sys
import environ
from pathlib import Path

# 1. Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Add 'apps' to Python Path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 3. Initialize Environment Variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# 4. Security
SECRET_KEY = env('SECRET_KEY', default='django-insecure-v2nf($8m8792o(zr0#etqvx9c*%23zku#(&d5a^9%-)5s9axiq')

# Production mein DEBUG False hona chahiye
DEBUG = env.bool('DEBUG', default=False)

# Railway domain aur localhost allow karne ke liye
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# 5. Application Definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-Party Apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    'django_celery_beat', 

    # Local Apps
    'notifications',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static files ke liye zaroori
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# 6. Database Configuration (Railway Optimized)
# Ye automatically DATABASE_URL uthayega jo Railway provide karta hai
DATABASES = {
    'default': env.db_url('DATABASE_URL', default=f"mysql://{env('MYSQLUSER')}:{env('MYSQLPASSWORD')}@{env('MYSQLHOST')}:{env('MYSQLPORT')}/{env('MYSQLDATABASE')}")
}

# 7. Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# 8. Celery & Redis Configuration
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULE = {
    'send-reminders-every-day': {
        'task': 'notifications.tasks.send_deadline_reminders',
        'schedule': 86400.0,
    },
}

# 9. Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# 10. Static & Files (WhiteNoise Setup)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
# Live server par static files serve karne ke liye engine
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# CSRF security for Production
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True