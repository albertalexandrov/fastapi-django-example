PROJECT_NAME = "ДЕМО"
MIDDLEWARES = [
    'django.middleware.security.SecurityMiddleware',
]
ROOT = "/api"
UVICORN_WORKERS = 2
UVICORN_HOST = "localhost"
UVICORN_PORT = 8000
UVICORN_RELOAD = True
API_DOCS_ENABLED = True
ENVIRONMENT = "LOCAL"
API_VERSION = "0.1.0"