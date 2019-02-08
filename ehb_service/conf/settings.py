import os
import environ

from django.core.exceptions import ImproperlyConfigured

from base import *

env = environ.Env()
env.read_env('{0}.env'.format(env('APP_ENV')))

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])
TIME_ZONE = env('TIME_ZONE', default='America/New_York')
DEBUG = env('DEBUG', default=True)
DATABASES = {
    'default': env.db()
}
SECRET_KEY = env('SECRET_KEY')
# LDAP Authentication Backend
LDAP = {
    'DEBUG': env('LDAP_DEBUG'),
    'PREBINDDN': env('LDAP_PREBINDDN'),
    'SEARCHDN': env('LDAP_SEARCHDN'),
    'SEARCH_FILTER': env('LDAP_SEARCH_FILTER'),
    'SERVER_URI': env('LDAP_SERVER_URI'),
    'PREBINDPW': env('LDAP_PREBINDPW')
}
EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env('EMAIL_PORT', default=25)
EMAIL_DOMAIN = 'email.chop.edu'
EHB_USE_ENCRYPTION = env('EHB_USE_ENCRYPTION', default=False)
EHB_ENCRYPTION_SERVICE = {
    'class': 'AESEncryption',
    'kwargs': {
        'use_checksum': True
    },
    'module': 'core.encryption.EncryptionServices'
}
EHB_KEY_MANAGEMENT_SERVICE = {
    'class': 'LocalKMS',
    'kwargs': {
        'key': env('EHB_KMS_SECRET')
    },
    'module': 'core.encryption.KMServices'
}
EHB_PROPS = {
    "EHB_GROUP_CLIENT_KEYS": {
        "salt_length": 12,
        "seed": env('EHB_CLIENT_KEY_SEED', default=1)
    },
    "EHB_GROUP_EHB_KEYS": {
        "length": 16,
        "seed": env('EHB_GROUP_KEY_SEED', default=1)
    }
}
FORCE_SCRIPT_NAME = env('FORCE_SCRIPT_NAME', default='')

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = env('REDIS_HOST', default='localhost')
SESSION_REDIS_PORT = env('REDIS_PORT', default=6379)

SESSION_COOKIE_NAME = 'ehb_sessionid'

if FORCE_SCRIPT_NAME:
    ADMIN_MEDIA_PREFIX = os.path.join(FORCE_SCRIPT_NAME, ADMIN_MEDIA_PREFIX[1:])
    STATIC_URL = os.path.join(FORCE_SCRIPT_NAME, STATIC_URL[1:])
    MEDIA_URL = os.path.join(FORCE_SCRIPT_NAME, MEDIA_URL[1:])

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.APITokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}
