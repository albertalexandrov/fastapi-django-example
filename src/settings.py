from functools import partial

from environs import Env
from fastapi_django.constants import EnvironmentEnum
from starlette.middleware.trustedhost import TrustedHostMiddleware

env = Env()
env.read_env(".env", override=True)

ENVIRONMENT = EnvironmentEnum.get_environment()

API_TITLE = env.str("API_TITLE", default="API title")
API_SUMMARY = env.str("API_SUMMARY", default="API summary")
API_DESCRIPTION = env.str("API_DESCRIPTION", default="API description")
API_VERSION = env.str("API_VERSION", default="0.1.0")
API_DOCS_ENABLED = env.bool("API_DOCS_ENABLED", default=False)
API_PREFIX = env.str("API_PREFIX", default="/api")

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

UVICORN_APP = "web.app:app"
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
        "typer": "management.cli:typer",
        # "name": "project-commands",  # объединение команд проекта в группу команд под названием project-commands
    }
]
