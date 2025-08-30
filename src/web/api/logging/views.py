import logging

import httpx
from fastapi import APIRouter, Depends
from fastapi import Request
from kz.auth.usr_adm import UsrAdmAuth
from fastapi_django.logging import logging_context

router = APIRouter(tags=["Логирование"])


@router.get("/logging", dependencies=[Depends(UsrAdmAuth())])
async def test_logging(request: Request):
    # предварительно в глобальном контексте логирования есть service_name и request_id
    with logging_context(num=1):
        logging.info("лог с контекстом")
        # выведет сообщение
        # {
        #     ...
        #     "message": "лог с контекстом",
        #     "service_name": "fastapi-django-example"
        #     "request_id": "8c54e50cb1494026accb25bad4ec685a",
        #     "num": 1
        # }
    logging.info("лог БЕЗ контекста")
    # выведет сообщение:
    # {
    #     ...
    #     "message": "лог БЕЗ контекстом",
    #     "service_name": "fastapi-django-example",
    #     "request_id": "8c54e50cb1494026accb25bad4ec685a"
    # }
    return logging_context


@router.get("/logging/e2e")
async def e2e_logging():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8001/api/v1/libs/regions")
    if resp.status_code != 200:
        return resp.status_code
    return resp.json()


@router.get("/logging/request-id-to-sentry")
async def request_id_to_sentry():
    # провоцируем исключение, чтобы x-request-id был добавлен в теги события sentry
    1/0
