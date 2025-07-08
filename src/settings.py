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

ENGINE = {
    "DRIVER": "django.db.backends.postgresql",
    "NAME": "mydatabase",
    "USER": "mydatabaseuser",
    "PASSWORD": "mypassword",
    "HOST": "127.0.0.1",
    "PORT": "5432",
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
