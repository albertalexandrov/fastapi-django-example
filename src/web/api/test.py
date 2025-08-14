import logging

from fastapi import APIRouter
from fastapi_django.conf import settings

router = APIRouter(tags=['Тест'])
logger = logging.getLogger(__name__)


@router.get('/test')
async def test():
    logger.warning("test")
    return settings.MIDDLEWARES
