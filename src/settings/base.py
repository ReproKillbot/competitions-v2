import os
import sys

import dj_database_url
from django.core.files.storage import get_storage_class


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Also add ../../apps to python path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# =============================================================================
# Django
# =============================================================================
ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = True

SITE_ID = 1

THIRD_PARTY_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'rest_framework',
    'whitenoise',
    'oauth2_provider',
    'corsheaders',
    'social_django',
    'django_extensions',
    'django_filters',
)
OUR_APPS = (
    'competitions',
    'datasets',
    'pages',
    'profiles',
    'leaderboards',
)
INSTALLED_APPS = THIRD_PARTY_APPS + OUR_APPS

MIDDLEWARE = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SECRET_KEY = os.environ.get("SECRET_KEY", '(*0&74%ihg0ui+400+@%2pe92_c)x@w2m%6s(jhs^)dc$&&g93')

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')

DEFAULT_FROM_EMAIL = 'Do Not Reply <donotreply@imagefirstuniforms.com>'
SERVER_EMAIL = 'Do Not Reply <donotreply@imagefirstuniforms.com>'

LOGIN_REDIRECT_URL = '/'

# AUTH_USER_MODEL = 'profiles.User'

# =============================================================================
# Authentication
# =============================================================================
AUTHENTICATION_BACKENDS = (
    # 'social_core.backends.github.GithubOAuth2',
    'utils.oauth_backends.ChahubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Github
SOCIAL_AUTH_GITHUB_KEY = os.environ.get('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['user']

# Generic
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

SOCIAL_AUTH_CODALAB_KEY = os.environ.get('SOCIAL_AUTH_CODALAB_KEY')
SOCIAL_AUTH_CODALAB_SECRET = os.environ.get('SOCIAL_AUTH_CODALAB_SECRET')

SOCIAL_AUTH_CHAHUB_BASE_URL = os.environ.get('SOCIAL_AUTH_CHAHUB_BASE_URL', 'https://codalabchahub.herokuapp.com')

# User Models
AUTH_USER_MODEL = 'profiles.User'
SOCIAL_AUTH_USER_MODEL = 'profiles.User'

# SOCIAL_AUTH_ALWAYS_ASSOCIATE = True


# =============================================================================
# Debugging
# =============================================================================
DEBUG = os.environ.get('DEBUG', True)


# =============================================================================
# Database
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USERNAME', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': 5432
    }
}
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)


# =============================================================================
# SSL
# =============================================================================
if os.environ.get('USE_SSL'):
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    # Allows us to use with django-oauth-toolkit on localhost sans https
    SESSION_COOKIE_SECURE = False

# ============================================================================
# Celery
# ============================================================================
BROKER_URL = os.environ.get("RABBITMQ_BIGWIG_URL", 'amqp://admin:admin@rabbitmq:5672/comps')
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'


# =============================================================================
# DRF
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DATETIME_INPUT_FORMATS': (
        'iso-8601',
        '%B %d, %Y',
    )
}

# OAuth Toolkit
OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}


# =============================================================================
# OAuth
# =============================================================================
CORS_ORIGIN_ALLOW_ALL = True

if not DEBUG and CORS_ORIGIN_ALLOW_ALL:
    raise Exception("Disable CORS_ORIGIN_ALLOW_ALL if we're not in DEBUG mode")


# =============================================================================
# Storage
# =============================================================================
DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.TemporaryFileUploadHandler",)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'

# S3 from AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_STORAGE_PRIVATE_BUCKET_NAME = os.environ.get('AWS_STORAGE_PRIVATE_BUCKET_NAME')
AWS_S3_CALLING_FORMAT = os.environ.get('AWS_S3_CALLING_FORMAT', 'boto.s3.connection.OrdinaryCallingFormat')
AWS_S3_HOST = os.environ.get('AWS_S3_HOST', 's3-us-west-2.amazonaws.com')
AWS_QUERYSTRING_AUTH = os.environ.get(
    # This stops signature/auths from appearing in saved URLs
    'AWS_QUERYSTRING_AUTH',
    False
)
if isinstance(AWS_QUERYSTRING_AUTH, str) and 'false' in AWS_QUERYSTRING_AUTH.lower():
    AWS_QUERYSTRING_AUTH = False  # Was set to string, convert to bool

# Azure
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', 'public')
BUNDLE_AZURE_ACCOUNT_NAME = os.environ.get('BUNDLE_AZURE_ACCOUNT_NAME', AZURE_ACCOUNT_NAME)
BUNDLE_AZURE_ACCOUNT_KEY = os.environ.get('BUNDLE_AZURE_ACCOUNT_KEY', AZURE_ACCOUNT_KEY)
BUNDLE_AZURE_CONTAINER = os.environ.get('BUNDLE_AZURE_CONTAINER', 'bundles')

# Helper booleans
STORAGE_IS_AWS = DEFAULT_FILE_STORAGE == 'storages.backends.s3boto.S3BotoStorage'
STORAGE_IS_AZURE = DEFAULT_FILE_STORAGE == 'storages.backends.azure_storage.AzureStorage'
STORAGE_IS_LOCAL = DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage'

# Setup actual storage classes we use on the project
StorageClass = get_storage_class(DEFAULT_FILE_STORAGE)

if STORAGE_IS_AWS:
    BundleStorage = StorageClass(bucket=AWS_STORAGE_PRIVATE_BUCKET_NAME)
    PublicStorage = StorageClass(bucket=AWS_STORAGE_BUCKET_NAME)
elif STORAGE_IS_AZURE:
    BundleStorage = StorageClass(account_name=BUNDLE_AZURE_ACCOUNT_NAME,
                                 account_key=BUNDLE_AZURE_ACCOUNT_KEY,
                                 azure_container=BUNDLE_AZURE_CONTAINER)

    PublicStorage = StorageClass(account_name=AZURE_ACCOUNT_NAME,
                                 account_key=AZURE_ACCOUNT_KEY,
                                 azure_container=AZURE_CONTAINER)
else:
    BundleStorage = StorageClass()
    PublicStorage = StorageClass()
