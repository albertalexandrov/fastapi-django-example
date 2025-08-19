from pydantic import BaseModel


class SendMailDataSchema(BaseModel):
    subject: str = "Тема письма"
    body: str = "Текст письма"
    recipient_list: list[str] = ["alber.aleksandrov@x5.ru"]
