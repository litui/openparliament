import os

DEBUG = True

ADMINS = [
    ('Michael Mulley', 'michael@michaelmulley.com'),
]

MANAGERS = ADMINS

PROJ_ROOT = os.path.dirname(os.path.realpath(__file__))

HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SITECONF = 'parliament.search_sites'

CACHE_MIDDLEWARE_KEY_PREFIX = 'parl'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Set to True to disable functionality where user-provided data is saved
PARLIAMENT_DB_READONLY = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Montreal'

# Language code for this installation.
# MUST BE either 'en' or 'fr'
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.realpath(os.path.join(PROJ_ROOT, '..', '..', 'mediafiles'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATICFILES_DIRS = [os.path.join(PROJ_ROOT, 'static')]
STATIC_ROOT = os.path.realpath(os.path.join(PROJ_ROOT, '..', '..', 'staticfiles'))
STATIC_URL = '/static/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = []
COMPRESS_OFFLINE = True

PARLIAMENT_LANGUAGE_MODEL_PATH = os.path.realpath(os.path.join(PROJ_ROOT, '..', '..', 'language_models'))
PARLIAMENT_DISABLE_WORDCLOUD = True

APPEND_SLASH = False

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60*60*24*60  # 60 days

PARLIAMENT_API_HOST = 'api.openparliament.ca'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'parliament.accounts.middleware.AuthenticatedEmailMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'parliament.core.api.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'parliament.urls'

WSGI_APPLICATION = 'parliament.wsgi.application'

TEMPLATE_DIRS = [
    os.path.join(PROJ_ROOT, 'templates'),
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django_extensions',
    'haystack',
    'south',
    'sorl.thumbnail',
    'compressor',
    'parliament.core',
    'parliament.accounts',
    'parliament.hansards',
    'parliament.elections',
    'parliament.bills',
    'parliament.politicians',
    'parliament.activity',
    'parliament.alerts',
    'parliament.committees',
    'parliament.search',
    'parliament.text_analysis',
    'parliament.wordpress'
]

THUMBNAIL_SUBDIR = '_thumbs'
THUMBNAIL_PROCESSORS = (
    'sorl.thumbnail.processors.colorspace',
    'sorl.thumbnail.processors.autocrop',
    'parliament.core.thumbnail.crop_first',
    'sorl.thumbnail.processors.scale_and_crop',
    'sorl.thumbnail.processors.filters',
)

SOUTH_TESTS_MIGRATE = False
TEST_RUNNER = 'parliament.core.test_utils.TestSuiteRunner'
TEST_APP_PREFIX = 'parliament'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(module)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'parliament': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    },
}


