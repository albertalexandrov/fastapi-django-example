import logging

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
