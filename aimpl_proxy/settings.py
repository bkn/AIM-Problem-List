# Django settings for aimpl project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ROOT = os.path.dirname(__file__)
PROJECT_NAME = os.path.split(SITE_ROOT)[-1]


WEB_PROXY_DOMAIN = '127.0.0.1'
WEB_PROXY_PORT = 5984
WEB_PROXY_BASE = 'aimpl/_design/aimpl'
WEB_PROXY_INDEX = '/pl'
WEB_PROXY_DB = "aimpl"

LATEX_TO_JSON_CMD = os.path.normpath(os.path.join(SITE_ROOT, "../../lib/make_pl.rb"))


ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

#MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(SITE_ROOT, 'aim.db')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


COUCHDB_DATABASES = (
     ('aimpl.pl', "http://%s:%s/%s" % (WEB_PROXY_DOMAIN, WEB_PROXY_PORT, WEB_PROXY_DB)),
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_LATEX =  os.path.join(MEDIA_ROOT, "latex")


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@asaxz4ua(4%tost8d#n@5f09e1@x(%&$a&yd3h4kva_x$l)!h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'aimpl_proxy.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates').replace('\\','/'),
    SITE_ROOT,
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'couchdbkit.ext.django',
    'aimpl_proxy.aimpl',
    'aimpl_proxy.registration',
)


ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'aimpl.org'
EMAIL_HOST_PASSWORD = 'riemann1234'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

LOGIN_REDIRECT_URL = '/pl/'
