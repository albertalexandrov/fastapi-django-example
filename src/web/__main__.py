import uvicorn


def main():
    uvicorn.run(
        "fastapi_django.app:application",
        workers=settings.UVICORN_WORKERS,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.UVICORN_RELOAD,
        factory=False,
        env_file='.env'
    )


if __name__ == "__main__":
    main()
