import os
import yaml

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

credentials = yaml.safe_load(open(os.path.join('credentials.yaml')))

SECRET_KEY = credentials['secret_key']

DEBUG =  credentials['debug']

ALLOWED_HOSTS =  credentials['allowed_hosts']

# Read from the gitignored credentials.yaml so this file can be committed.
# WARNING: changing this value makes every already-encrypted column in the
# database unreadable. It cannot be rotated without a re-encryption migration.
ENCRYPTION_KEY = credentials['encryption_key'].encode()

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    #Apps
    'accounts.apps.AccountsConfig',
    'servenline.apps.ServenlineConfig',
    'crispy_bootstrap5',
    'crispy_forms',
    # django-recaptcha renamed its app from 'captcha' to 'django_recaptcha' in
    # 4.0.0, which is the version pinned in requirements.txt and installed in
    # venv/. 'captcha' no longer resolves.
    'django_recaptcha',
    # 'axes',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

AUTH_USER_MODEL = "accounts.User"


DATABASES = {
    "default": {
        'ENGINE': credentials['db_engine'],
        'NAME': credentials['db_name'],
        'USER': credentials['db_username'],
        'PASSWORD': credentials['db_password'],
        'PORT': credentials['db_port'],
        'HOST': credentials['db_host'],
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = False


STATIC_URL = "static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Required by collectstatic, which the production stack runs so nginx can serve
# /static/ directly. Was missing entirely, so collectstatic errored out.
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'staticfiles'))

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = '/media/'


VALID_IMAGE_FORMAT = ['jpg', 'png', 'jpeg', 'heic', 'webp']

OTP_VALID_TILL = 600 #seconds

# accounts/utils.py reads settings.RATE_LIMIT_DURATION at import time, and
# accounts/views.py imports that module -- so without this every accounts view
# raised AttributeError. Seconds; pairs with utils.MAX_REQUESTS_PER_MINUTE = 5.
RATE_LIMIT_DURATION = 60

# accounts/utils.py rate limiter. Host is env-driven so the container can point
# at the 'redis' compose service; the default keeps local runs working.
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_DB = int(os.environ.get('REDIS_DB', 0))

# django-recaptcha falls back to Google's public test keys when these are
# unset, which trips a system check that refuses to start the server.
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')
if not (RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY):
    SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"





# --- Running behind the nginx reverse proxy -------------------------------
# Without these Django builds http:// URLs and rejects POSTs over HTTPS,
# because from gunicorn's point of view the connection is plain HTTP.
CSRF_TRUSTED_ORIGINS = credentials.get('csrf_trusted_origins', [])
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
