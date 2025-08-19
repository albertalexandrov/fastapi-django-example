import os
import shutil
from contextlib import asynccontextmanager
from pathlib import Path
from tempfile import gettempdir

from fastapi import FastAPI
from fastapi_django.conf import settings

from web.api.auth import auth_examples_router
from web.api.crud import crud_router
from web.api.permissions import permissions_examples_router
from web.api.sessions import session_examples_router
from web.api.test import router as test_router
from web.api.users import router as users_router
from web.api.mail import router as mail_router


def setup_prometheus(app: FastAPI) -> None:
    if not settings.PROMETHEUS_ENABLED:
        return
    prometheus_multiproc_dir = Path(gettempdir()) / "prometheus"
    shutil.rmtree(prometheus_multiproc_dir, ignore_errors=True)
    prometheus_multiproc_dir.mkdir(parents=True, exist_ok=True)
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = prometheus_multiproc_dir.as_posix()
    # сохранить переменную окружения PROMETHEUS_MULTIPROC_DIR необходимо до импорта Instrumentator,
    # тк на основе наличия переменной PROMETHEUS_MULTIPROC_DIR prometheus_client определяет ValueClass
    # https://github.com/prometheus/client_python/blob/73680284ce63f0bc0f23cfc42af06e74fd7e3ccf/prometheus_client/values.py#L139
    from prometheus_fastapi_instrumentator import Instrumentator
    instrumentator = Instrumentator(should_group_status_codes=False)
    instrumentator.instrument(app)
    instrumentator.expose(app, should_gzip=True, name="prometheus_metrics")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.middleware_stack = None
    setup_prometheus(app)
    app.middleware_stack = app.build_middleware_stack()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="fastapi-django example",
        lifespan=lifespan,
    )
    app.include_router(test_router)
    app.include_router(users_router)
    app.include_router(auth_examples_router)
    app.include_router(permissions_examples_router)
    app.include_router(session_examples_router)
    app.include_router(crud_router)
    app.include_router(mail_router)
    return app
