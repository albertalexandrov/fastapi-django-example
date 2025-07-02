from fastapi import APIRouter

router = APIRouter(tags=['Здоровье'])


@router.get("/healthcheck", status_code=200)
def health_check():
    return {"status": "alive"}
