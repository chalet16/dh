# Django settings for cookcrew project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Joel Cohen', 'jacohen@mit.edu'),
     ('David Ogutu','ogutu@mit.edu'),
)
# customized settings
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(PROJECT_ROOT)
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)

MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dh_db.sql',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/__scripts/django/static/admin/'
# Make this unique, and don't share it with anybody.
SECRET_KEY = '%rz*^s7r9w^cwz55!%i61gr659ov+vql1u9afcj$txy))sddmp'
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cl.mit.ScriptsRemoteUserMiddleware',
)
AUTHENTICATION_BACKENDS = (
	'cl.mit.ScriptsRemoteUserBackend',
	'django.contrib.auth.backends.ModelBackend',
)
#CHANGE THIS if the site is hosted at a root other than /essen
LOGIN_URL='/essen/accounts/login/'
ROOT_URLCONF = 'cl.urls'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATIC_ROOT = ''
STATIC_URL = '/static/essen/'
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cl.recipes',
    'cl.menus',
    'cl.schedules',
    #'cookcrew.assetpackager',
)

try:
    from local_settings import *
except ImportError:
    pass

