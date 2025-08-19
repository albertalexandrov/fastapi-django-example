import fastapi_django.mail
from fastapi import APIRouter
from fastapi_django import mail
from fastapi_django.mail import send_mail

from web.api.mail.schemas import SendMailDataSchema

router = APIRouter(tags=["Отправка электронных писем"])


@router.post("/mail/console")
async def send_console_mail(data: SendMailDataSchema):
    await send_mail(**data.model_dump(), provider="console")


@router.post("/mail/dummy")
async def send_dummy_mail(data: SendMailDataSchema):
    await send_mail(**data.model_dump(), provider="dummy")


@router.post("/mail/filebased")
async def send_filebased_mail(data: SendMailDataSchema):
    await send_mail(**data.model_dump(), provider="filebased")  # from_email="mail@from.ru",


@router.post("/mail/locmem")
async def send_locmem_mail(data: SendMailDataSchema):
    # для тестов.  после каждого теста необходимо очистить outbox:
    # https://pytest-django.readthedocs.io/en/stable/helpers.html#clearing-of-mail-outbox
    await send_mail(**data.model_dump(), provider="locmem")
    print("Письма в outbox:", mail.outbox)


@router.post("/mail/smtp")
async def send_smtp_mail(data: SendMailDataSchema):
    await send_mail(**data.model_dump(), provider="smtpsrv")


@router.post("/mail/kz")
async def send_kz_mail(data: SendMailDataSchema):
    from kz.mail import send_mail
    await send_mail(
        subject=data.subject,
        body=data.body,
        is_html=False,
        recipients=data.recipient_list,
    )


@router.post("/mail/nkz")
async def send_kz_mail(data: SendMailDataSchema):
    from nkz.mail import send_mail  # функция send_mail несет в себе специфику НКЗ (есть поле notification_subject в отличии от КЗ)
    await send_mail(
        subject=data.subject,
        body=data.body,
        is_html=False,
        recipients=data.recipient_list,
        notification_subject="test-send-mail"
    )
