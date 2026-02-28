from pathlib import Path
import os

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key secret!
SECRET_KEY = 'django-insecure-CHANGE-ME-1234567890'

DEBUG = False  # Set False in production

ALLOWED_HOSTS = ['*']


# ---------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # REST Framework
    'rest_framework',
    'rest_framework.authtoken',

    # Your apps
    'users',
    'gestures',
    'devices',
    'music_control',
]

AUTH_USER_MODEL = "users.CustomUser"


# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


# ---------------------------------------------------------
# URLS & WSGI
# ---------------------------------------------------------
ROOT_URLCONF = 'backend_project.urls'

WSGI_APPLICATION = 'backend_project.wsgi.application'


# ---------------------------------------------------------
# DATABASE 
# ---------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wave_tunes_db',
        'USER': 'postgres',
        'PASSWORD': 'Abhay@1909',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# ---------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------

AUTHENTICATION_BACKENDS = [
    'users.backend.EmailBackend',                 # custom email login
    'django.contrib.auth.backends.ModelBackend',   # default
]

# If you have a custom user model uncomment this:
# AUTH_USER_MODEL = "users.User"


# ---------------------------------------------------------
# REST FRAMEWORK CONFIG
# ---------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # global templates folder
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


# ---------------------------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',          # /backend/static/
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
