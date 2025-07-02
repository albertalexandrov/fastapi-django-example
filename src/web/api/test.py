from fastapi import APIRouter
from fastapi_xyz.conf import settings

router = APIRouter(tags=['Тест'])


@router.get('/test')
async def test():
    return settings.PROJECT_NAME