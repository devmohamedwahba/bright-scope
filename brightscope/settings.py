"""
Django settings for brightscope project.
"""

import environ, os, sys
import dj_database_url
from pathlib import Path
from django.core.management.utils import get_random_secret_key
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

######################################################################
# General
######################################################################
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ENVIRONMENT = env("ENVIRONMENT", default="local")
SECRET_KEY = env("SECRET_KEY", default=get_random_secret_key())
DEBUG = env("DEBUG", default="False").lower() == "true"

# Application definition
INSTALLED_APPS = [
    'material',
    'material.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    "rest_framework",
    'apps.account',
    'apps.contact_us',
    'apps.service',
    'apps.settings',
    'apps.payments',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
ROOT_URLCONF = 'brightscope.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'brightscope.wsgi.application'

# Database
if ENVIRONMENT.lower() == "local":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }

# Password validation
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

#######################################################################
# Localization
######################################################################
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

######################################################################
# Static
######################################################################
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

######################################################################
# Session & Authentication - FIXED VERSION
######################################################################
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_COOKIE_SECURE = True  # Force True for Heroku
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_NAME = 'brightscope_sessionid'
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF Settings - FIXED VERSION
CSRF_TRUSTED_ORIGINS = [
    "https://bright-scope-2c6c515b6aa6.herokuapp.com",
    "https://www.bright-scope-2c6c515b6aa6.herokuapp.com",
]
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True  # Force True for Heroku
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_NAME = 'brightscope_csrftoken'
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# Heroku specific settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Let Heroku handle redirects

# Remove domain settings
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = reverse_lazy('admin:login')
LOGIN_REDIRECT_URL = reverse_lazy('admin:index')
LOGOUT_REDIRECT_URL = reverse_lazy('admin:login')

######################################################################
# CORS Settings
######################################################################
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOWED_ORIGINS = [
    "https://bright-scope-2c6c515b6aa6.herokuapp.com",
]

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ])
    # Allow HTTP in development only
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

######################################################################
# Other Settings
######################################################################
ALLOWED_HOSTS = [
    'bright-scope-2c6c515b6aa6.herokuapp.com',
    '.bright-scope-2c6c515b6aa6.herokuapp.com',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

AUTH_USER_MODEL = 'account.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@brightscope.com')

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
}

PASSWORD_RESET_TIMEOUT = 900
FRONTEND_URL = env("FRONTEND_URL")
SITE_NAME = 'Bright Scope'

PAYTABS_PROFILE_ID = os.getenv("PAYTABS_PROFILE_ID")
PAYTABS_SERVER_KEY = os.getenv("PAYTABS_SERVER_KEY")
PAYTABS_BASE_URL = os.getenv("PAYTABS_BASE_URL", "https://secure.paytabs.com")
PAYTABS_CALLBACK_PATH = os.getenv("PAYTABS_CALLBACK_PATH")
PAYTABS_RETURN_PATH = os.getenv("PAYTABS_RETURN_PATH")

MATERIAL_ADMIN_SITE = {
    'HEADER': 'Bright Scope Admin',
    'TITLE': 'Bright Scope',
    'MAIN_BG_COLOR': '#3f51b5',
    'MAIN_HOVER_COLOR': '#303f9f',
    'SHOW_THEMES': True,
    'TRAY_REVERSE': True,
    'NAVBAR_REVERSE': True,
    'SHOW_COUNTS': True,
}

# Logging - Enable for debugging
ENABLE_LOGGING = True  # Force enable for debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Heroku configuration
import django_heroku
django_heroku.settings(locals(), staticfiles=False)