# Django settings for intranet project.

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'../..')))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEV_SITE = True

ADMINS = (
    ('Alex Ashley', 'alex@ashley-family.net'),
)

INTERNAL_IPS = ( '127.0.0.1', )

MANAGERS = ADMINS
DATABASES = {
             'default': {
                        'ENGINE':'django.db.backends.sqlite3',
                        'NAME':'djangotest',
                         }
             }
    
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

MEDIA_ROOT = os.getcwd()
STATIC_ROOT = os.path.join(MEDIA_ROOT,'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/django/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#skjhdskhkjhk'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

CACHE_MIDDLEWARE_SECONDS=300
CACHE_MIDDLEWARE_KEY_PREFIX=''
NETWORK_MASK='255.255.255.0'

TEMPLATE_DIRS = (
                 # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
                 # Always use forward slashes, even on Windows.
                 # Don't forget to use absolute paths, not relative paths.
                   os.getcwd()
                 )
CACHES = {
              'default': {
                          'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                          'LOCATION': 'addressbook-demo'
                          },
              }    
#STATICFILES_DIRS = ('/home/net/xjjeno/alex/WORK/workspace/Intranet/media/',)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.debug",
        "django.core.context_processors.request",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.contrib.auth.context_processors.auth",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'djangoutil',
    'addressbook',
)
