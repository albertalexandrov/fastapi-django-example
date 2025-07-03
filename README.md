# Todo:

1. обработать пустое значение settings.api.root и значения с или без слеша
2. для классов с конфигами можно выделять обязательные настройки и необязательные и их нужно как то обозвать одним словом



варианты получения настроек внешними либами:

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    # Add data like request headers and IP for users;
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

или:

cloudinary.config(
  cloud_name = 'your-cloud-name',
  api_key = 'your-api-key',
  api_secret = 'your-api-secret'
)

Авторизация в ПП в отдельной библиотеке напр nkz, тк там могут быть свои особенности

Инстанс FastAPI конфигурируется с заданными параметрами из настроек. 
Но должна быть возможность доконфигурировать приложение при необходимости