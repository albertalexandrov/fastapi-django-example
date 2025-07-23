
from pathlib import Path

from benedict import benedict
from fastapi import FastAPI, APIRouter
from fastapi_django.app import get_default_app
from fastapi_django.conf import settings
from prometheus_fastapi_instrumentator import PrometheusFastApiInstrumentator
from starlette.requests import Request
from starlette.responses import JSONResponse

from web.api.test import router as test_router
from web.api.users import router as users_router
from web.api.auth import auth_examples_router
from web.api.sessions import session_examples_router
from web.api.permissions import permissions_examples_router
from web.api.crud import crud_router
from web.i18n import locale
from web.middlewares import example_middleware

APP_ROOT = Path(__file__).parent

# todo: обработчики можно вынести в библиотеку в папку faststream, например


def request_validation_error_handler(request: Request, exc):
    errors = locale.translate(exc.errors(), "ru_RU")
    content = benedict()
    for error in errors:
        key = []
        for item in error["loc"][1:]:
            key.append(item)
        key = '.'.join(key)
        content[key] = error["msg"]
    return JSONResponse(content, status_code=422)


def include_routers(app: FastAPI):
    router = APIRouter(prefix=settings.ROOT)
    router.include_router(test_router)
    app.include_router(router)


def add_middlewares(app: FastAPI):
    app.middleware("http")(example_middleware)


def setup_prometheus(app: FastAPI) -> None:  # pragma: no cover
    instrumentator = PrometheusFastApiInstrumentator(should_group_status_codes=False)
    instrumentator = instrumentator.instrument(app)
    instrumentator.expose(app, should_gzip=True, name="prometheus_metrics", tags=["Метрики"])


# def get_app() -> FastAPI:
#     # if settings.sentry_dsn:
#     #     sentry_sdk.init(
#     #         dsn=settings.sentry_dsn,
#     #         traces_sample_rate=0.1,
#     #         environment=settings.environment,
#     #         integrations=[
#     #             StarletteIntegration(),
#     #             FastApiIntegration(transaction_style="endpoint"),
#     #             LoggingIntegration(level=logging.getLevelName(settings.log_level)),
#     #             SqlalchemyIntegration(),
#     #         ],
#     #     )
#     app = FastAPI(
#         title=settings.PROJECT_NAME,
#         docs_url=None,
#         openapi_url=f"{settings.ROOT}/docs/openapi.json",
#         redoc_url=None,
#         version=settings.API_VERSION,
#         # exception_handlers={
#         #     RequestValidationError: request_validation_error_handler,
#         #     RequestBodyValidationError: request_body_validation_error_handler,
#         #     NotFoundError: not_found_error_handler,
#         #     AnyBodyBadRequestError: any_body_bad_request_exception_handler,
#         # },
#     )
#     print(app.openapi_url)
#     include_routers(app)
#     add_middlewares(app)
#     setup_prometheus(app)
#     return app


# 1. создается приложение с указанными или дефолтными настройками
app = get_default_app()
# 2. созданное приложение доконфигурируется, напр., добавляются урлы
app.include_router(test_router)
app.include_router(users_router)
app.include_router(auth_examples_router)
app.include_router(permissions_examples_router)
app.include_router(session_examples_router)
app.include_router(crud_router)
