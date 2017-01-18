"""
Django settings for hostedfactor project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from urllib.parse import urlparse
import logging
from environs import Env

logger = logging.getLogger(__name__)

# Environment reading. Automatically read from .env file if available
env = Env()
try:
    env.read_env()
    logger.info('.env file read into environment')
except FileNotFoundError:
    logger.info('No .env file found to read environment found')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# Turn on debug if explicitly enabled or if we are a dev server
# SECURITY WARNING: don't run with debug turned on in production!
SERVER_MODE = env.str('SERVER_MODE', 'prod')
DEBUG = env.bool('DEBUG', SERVER_MODE == 'dev')

ALLOWED_HOSTS = [
    'localhost',
    '*',
]

# Security settings
# If we're using SSL, be strict about it
SECURE_HSTS_SECONDS = 0
SECURE_SSL_REDIRECT = SERVER_MODE == 'prod'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#USE_X_FORWARDED_HOST = SECURE_SSL_REDIRECT # For Heroku, we wouldn't receive requests that don't match us
USE_X_FORWARDED_PORT = SECURE_SSL_REDIRECT
SECURE_REDIRECT_EXEMPT = [
    '^.well-known/',
]

SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE

CSRF_COOKIE_HTTPONLY = False # Need to access for JS
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'users',
    'codes',
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

# URLs
ROOT_URLCONF = 'hostedfactor.urls'
STATIC_URL = '/static/'
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Static files
STATIC_ROOT = env('STATIC_FILES', 'collectedstatic')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

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

WSGI_APPLICATION = 'hostedfactor.wsgi.application'

# If deployed and internet-accessible, use Rollbar
USE_ROLLBAR = env.bool('USE_ROLLBAR', False)
if USE_ROLLBAR:
    logger.info('Rollbar enabled')

    ROLLBAR_CLIENT_TOKEN = env('ROLLBAR_POST_CLIENT_ITEM_ACCESS_TOKEN', False)
    if not ROLLBAR_CLIENT_TOKEN:
        logger.warn('Javascript Rollbar reporting disabled, ROLLBAR_POST_CLIENT_ITEM_ACCESS_TOKEN not given')

    ROLLBAR = {
        'access_token': env('ROLLBAR_POST_SERVER_ITEM_ACCESS_TOKEN'),
        'environment': SERVER_MODE,
        'branch': 'master',
        'root': BASE_DIR,
        'code_version': VERSION_INFO['commit'],
    }

    MIDDLEWARE.append('rollbar.contrib.django.middleware.RollbarNotifierMiddleware')
else:
    logger.info('Rollbar disabled')

# Email gets sent to SMTP if configured, console otherwise
DEFAULT_FROM_EMAIL = env('EMAIL_FROM', 'noreply@hostedfactor.io')
if env('USE_SMTP', False):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT', 587)
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS', True)
    EMAIL_USE_SSL = env('EMAIL_USE_SSL', False)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
DATABASE_URL = urlparse(env('DATABASE_URL', 'postgres://postgres:postgres@db:5432/postgres'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_URL.path[1:],
        'USER': DATABASE_URL.username,
        'PASSWORD': DATABASE_URL.password,
        'HOST': DATABASE_URL.hostname,
        'PORT': DATABASE_URL.port if DATABASE_URL.port else 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'