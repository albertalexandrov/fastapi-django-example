import logging
from functools import partial

from environs import Env
from fastapi_django.constants import EnvironmentEnum
from starlette.middleware.trustedhost import TrustedHostMiddleware

env = Env()
env.read_env(".env", override=True)

ENVIRONMENT = EnvironmentEnum.get_environment()

API_TITLE = env.str("API_TITLE", default="API title")
API_DOCS_ENABLED = env.bool("API_DOCS_ENABLED", default=False)
API_PREFIX = env.str("API_PREFIX", default="/api")

LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")

DATABASE = {
    "DRIVERNAME": "postgresql+asyncpg",
    "DATABASE": env.str("DATABASE_NAME"),
    "USERNAME": env.str("DATABASE_USERNAME"),
    "PASSWORD": env.str("DATABASE_PASSWORD"),
    "HOST": env.str("DATABASE_HOST"),
    "PORT": env.str("DATABASE_PORT", "5432"),
    "OPTIONS": {
        "echo": env.bool("DATABASE_ECHO", False),
    },
}

UVICORN_APP = "web.app:create_app"
UVICORN_WORKERS = env.int("UVICORN_WORKERS", default=1)
UVICORN_HOST = env.str("UVICORN_HOST", default="localhost")
UVICORN_PORT = env.int("UVICORN_PORT", default=8000)
UVICORN_RELOAD = env.bool("UVICORN_RELOAD", default=True)

PROMETHEUS_ENABLED = env.bool("PROMETHEUS_ENABLED", default=False)

MIDDLEWARES = [
    partial(TrustedHostMiddleware, allowed_hosts=["localhost", "*.example.com"])
]

USR_ADM_AUTH_HOST = env.str("USR_ADM_AUTH_HOST", default="http://localhost")
USR_ADM_AUTH_USERNAME = env.str("USR_ADM_AUTH_USERNAME", default="username")
USR_ADM_AUTH_PASSWORD = env.str("USR_ADM_AUTH_PASSWORD", default="password")
USR_ADM_AUTH_VERIFY = env.bool("USR_ADM_AUTH_VERIFY", default=True)
USR_ADM_AUTH_REALM_URL = env.str("USR_ADM_AUTH_REALM_URL", default="http://localhost")

INTEGRATION_USER_USERNAME = env.str("INTEGRATION_USER_USERNAME")
INTEGRATION_USER_PASSWORD = env.str("INTEGRATION_USER_PASSWORD")

MANAGEMENT = [
    {
        "TYPER": "management.cli:typer",
        # "NAME": "project-commands",  # объединение команд проекта в группу команд под названием project-commands
    }
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "reserved_attrs": [],  # в лог добавляются все поля
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            # "formatter": "json",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# бекенды для непосредственной (немедленной, в отличии от отправки писем в КЗ) отправки электронных писем
# на одном уровне с ключом BACKEND предлагается прописывать обязательные параметры, а в OPTIONS - необязательные
# в Django 6 должны появиться мультибекенды для отпарвки электронных писем https://github.com/django/django/pull/18421/

EMAIL_PROVIDERS = {
    'console': {
        'BACKEND': 'fastapi_django.mail.backends.console.EmailBackend',
    },
    'dummy': {
        'BACKEND': 'fastapi_django.mail.backends.dummy.EmailBackend',
    },
    'filebased': {
        'BACKEND': 'fastapi_django.mail.backends.filebased.EmailBackend',
        "OPTIONS": {
            "file_path": "mails",
        }
    },
    'locmem': {
        'BACKEND': 'fastapi_django.mail.backends.locmem.EmailBackend',
    },
    'smtpsrv': {
        'BACKEND': 'fastapi_django.mail.backends.smtp.EmailBackend',
        "HOST": env.str("SMTPSRV_HOST"),
        "PORT": env.str("SMTPSRV_PORT"),
        "OPTIONS": {
            "username": env.str("SMTPSRV_USERNAME"),
            "password": env.str("SMTPSRV_PASSWORD"),
            "from_email": env.str("SMTPSRV_FROM_EMAIL"),
        },
    },
}

# отправка электронных писем в сервис Mailing (специфично для КЗ)
# для отправки писем используется функция kz.mail.send_mail

KZ_MAILING_BACKEND = "kz.mail.backends.rmq.EmailBackend"
KZ_MAILING_RMQ_HOST = env.str("KZ_MAILING_RMQ_HOST", "localhost")
KZ_MAILING_RMQ_PORT = env.int("KZ_MAILING_RMQ_PORT", 5672)
KZ_MAILING_RMQ_USERNAME = env.str("KZ_MAILING_RMQ_USERNAME", "guest")
KZ_MAILING_RMQ_PASSWORD = env.str("KZ_MAILING_RMQ_PASSWORD", "guest")
KZ_MAILING_SERVICE_NAME = "fastapi-django-example"
KZ_MAILING_FROM_EMAIL = env.str("KZ_MAILING_FROM_EMAIL")
KZ_MAILING_LIFE_TIME = env.int("KZ_MAILING_LIFE_TIME", 30)
KZ_MAILING_RMQ_TIMEOUT = env.int("KZ_MAILING_RMQ_TIMEOUT", 5)

# отправка электронных писем в сервис уведомлений (специфично для НКЗ)
# данные отправляются в сервис по http

NKZ_MAILING_BACKEND = "nkz.mail.backends.ntfsrvc.EmailBackend"
NKZ_MAILING_HOST = env.str("NKZ_MAILING_HOST", "localhost")
NKZ_MAILING_USERNAME = env.str("NKZ_MAILING_USERNAME", "username")
NKZ_MAILING_PASSWORD = env.str("NKZ_MAILING_PASSWORD", "password")
NKZ_MAILING_SERVICE_NAME = "fastapi-django-example"
NKZ_MAILING_LIFE_TIME = env.int("NKZ_MAILING_LIFE_TIME", 30)
NKZ_MAILING_TIMEOUT = env.int("NKZ_MAILING_TIMEOUT", 5)
NKZ_MAILING_VERIFY = env.bool("NKZ_MAILING_VERIFY", True)
