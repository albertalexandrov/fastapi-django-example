import logging
import os
import shutil
from contextlib import asynccontextmanager
from pathlib import Path
from tempfile import gettempdir

import sentry_sdk
from fastapi import FastAPI
from fastapi_django.conf import settings
from kz.logging.httpx import add_request_id_to_request
from kz.logging.sentry import add_request_id_to_event
from kz.middlewares import LoggingMiddleware, ExceptionMiddleware
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette_context.middleware import ContextMiddleware
from starlette_context.plugins import RequestIdPlugin

from web.api.auth import auth_examples_router
from web.api.bell import router as bell_router
from web.api.crud import crud_router
from web.api.logging import router as logging_router
from web.api.mail import router as mail_router
from web.api.permissions import permissions_examples_router
from web.api.sessions import session_examples_router
from web.api.templates import router as templates_router
from web.api.test import router as test_router
from web.api.users import router as users_router

logger = logging.getLogger(__name__)


def setup_prometheus(app: FastAPI) -> None:
    if not settings.PROMETHEUS_ENABLED:
        logger.info("Prometheus не был проинициализирован")
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
    logger.info("Prometheus проинициализирован")


def setup_sentry() -> None:
    if not settings.SENTRY_DSN:
        logger.info("Sentry не был проинициализирован")
        return
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
        environment=settings.ENVIRONMENT,
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            LoggingIntegration(
                level=settings.LOG_LEVEL,
                event_level=logging.ERROR,
            ),
            SqlalchemyIntegration(),
        ],
        before_send=add_request_id_to_event,
    )
    logger.info("Sentry проинициализирован")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.middleware_stack = None
    setup_prometheus(app)
    app.middleware_stack = app.build_middleware_stack()
    yield


def add_middlewares(app: FastAPI):
    # запрос проходит снизу вверх
    app.add_middleware(ExceptionMiddleware)  # добавит в лог исключения идентификатор запроса request_id
    app.add_middleware(LoggingMiddleware)  # создаст контекст логирования, куда будет помещен идентификатор запроса request_id
    app.add_middleware(ContextMiddleware, plugins=[RequestIdPlugin()])  # создаст контекст запроса


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
    app.include_router(bell_router)
    app.include_router(templates_router)
    app.include_router(logging_router)
    add_middlewares(app)
    add_request_id_to_request()
    setup_sentry()
    return app
