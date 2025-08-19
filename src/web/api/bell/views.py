from fastapi import APIRouter
from kz.bell import send_bell, outbox

router = APIRouter(tags=["Колокольчик"])


@router.get("/bell")
async def send_bell_notification():
    await send_bell(headline="Заголовок", text="Текст", users=["alber.aleksandrov@x5.ru"])
    print(outbox)