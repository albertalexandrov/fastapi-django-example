from fastapi import APIRouter
from fastapi_django.conf import settings

router = APIRouter(tags=['Тест'])


@router.get('/test')
async def test():
    return settings.MIDDLEWARES