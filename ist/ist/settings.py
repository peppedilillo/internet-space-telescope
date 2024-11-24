"""
Django project settings.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# p: pull the secret key from environment
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# p: pull debug config from environment
DEBUG = bool(int(os.environ.get("DEBUG", 0)))

# p: pull allowed hosts from environment
ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get("ALLOWED_HOSTS", "").split(","),
    )
)
if DEBUG:
    # p: for testing on mobile
    ALLOWED_HOSTS.extend(["*"])


# Application definition
INSTALLED_APPS = [
    "mboard.apps.AppConfig",
    "demo.apps.DemoConfig",
    "accounts.apps.AccountsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # for tracking comments and posts edits
    "pghistory",
    "pgtrigger",
]


if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    DEBUG_TOOLBAR_CONFIG = {
        "IS_RUNNING_TESTS": False,
    }


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # rate limiter
    "mboard.middleware.rate_limiter",
]

if DEBUG:
    MIDDLEWARE += [
        "pyinstrument.middleware.ProfilerMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

ROOT_URLCONF = "ist.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "ist.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# p: again, pulls database info from environment

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# p: double static is because we will use the first one to unambiguously catch
# p: requests that should be addressed to nginx proxy
STATIC_URL = "static/static/"

if not DEBUG:
    STATIC_ROOT = "/vol/web/static"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# p: redirect to home URL after login (default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = "/"

# p: this will redirect emails to the console.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# p: custom user model
AUTH_USER_MODEL = "accounts.CustomUser"

if DEBUG:
    # :p needed by debug toolbar
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

# Caches
# p: again we get these from the environment
CACHE_HOST = os.environ.get('CACHE_HOST')
CACHE_PASS = os.environ.get('CACHE_PASS')

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{CACHE_PASS}@{CACHE_HOST}",
    }
}
