"""
Django settings for gettingstarted project, on Heroku. Fore more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import dj_database_url


LEAGUE_URL = os.environ.get('LEAGUE_URL')
NFL_USER   = os.environ.get('NFL_USER')
NFL_PASS   = os.environ.get('NFL_PASS')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG           = False
TEMPLATE_DEBUG  = False


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'gettingstarted.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'hello.context_processors.custom',
            ],
        },
    },
]

WSGI_APPLICATION = 'gettingstarted.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE   = 'en-us'
TIME_ZONE       = 'Europe/Copenhagen'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True


# Parse database configuration from $DATABASE_URL
DATABASES = {'default' :  dj_database_url.config() }

# Enable Connection Pooling (if desired)
#DATABASES['default']['ENGINE'] = 'django_postgrespool'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

ENV_PTH     = os.path.abspath(os.path.dirname(__file__))
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))


MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
MEDIA_URL  = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

#SHOW_RESULTS = os.environ['show_results']
SHOW_RESULTS            = 1
SHOW_RESULTS_FOR_SU     = 1
SHOW_RESULTS_FOR_STAFF  = 1
LOCK_BIDS               = 0
IS_LOCAL                = False


if os.environ.get('IS_LOCAL'):
    passwd = os.environ.get('DB_PASS')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'waiver',   
            'USER': 'jkr',
            'PASSWORD': passwd,
            'HOST': 'localhost',
            'PORT': '',    }
    }
    DEBUG           = True
    TEMPLATE_DEBUG  = True
    IS_LOCAL        = True
