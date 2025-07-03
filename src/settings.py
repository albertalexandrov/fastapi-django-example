from environs import Env
from fastapi_django.constants import EnvironmentEnum

env = Env()
env.read_env(".env", override=True)

ENVIRONMENT = EnvironmentEnum.get_environment()

API_TITLE = env.str("API_TITLE", default="API title")
API_SUMMARY = env.str("API_SUMMARY", default="API summary")
API_DESCRIPTION = env.str("API_DESCRIPTION", default="API description")
API_VERSION = env.str("API_VERSION", default="0.1.0")
API_DOCS_ENABLED = env.bool("API_DOCS_ENABLED", default=False)
API_PREFIX = env.str("API_PREFIX", default="/api")

UVICORN_WORKERS = env.int("UVICORN_WORKERS", default=1)
UVICORN_HOST = env.str("UVICORN_HOST", default="localhost")
UVICORN_PORT = env.int("UVICORN_PORT", default=8000)
UVICORN_RELOAD = env.bool("UVICORN_RELOAD", default=True)
