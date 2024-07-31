import os
from pathlib import Path

from loguru import logger

from .project_settings.allauth import *
from .project_settings.common import *
from .utils.logging import setup_logging


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    'handlers': {
        'intercept': {
            '()': setup_logging(logger),
            'level': 'DEBUG',
        },
    },
    "console": {
        "level": "INFO",
        "filters": ["require_debug_true"],
        "class": "logging.StreamHandler",
        "formatter": "simple",
    },
    "mail_admins": {
        "level": "ERROR",
        "class": "django.utils.log.AdminEmailHandler",
        "filters": ["special", "console"],
    },

    "loggers": {
        "":
            {
                "handlers": ["intercept", ],
                "level": "DEBUG",
                "propagate": True,
            },
        "django": {
            "handlers": ["intercept", ],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["intercept", ],
            "level": "DEBUG",
            "propagate": False,
        },
        "core": {
            "handlers": ["intercept", ],
            "level": "DEBUG",
            "propagate": False,
        },

    },
}

if os.getenv('DJANGO_ENVIRONMENT') == 'development':
    logger.info('Loading development settings.')
    from .project_settings.development import *
else:
    logger.info('Loading development settings.')
    from .project_settings.production import *

BASE_DIR = Path(__file__).resolve().parent.parent

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'core.utils.auth.middleware.RefreshTokenMiddleware',
]

INSTALLED_APPS = [
    "main.apps.MainConfig"]

INSTALLED_APPS += INSTALLED_APPS_SHARED

