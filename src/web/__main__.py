import uvicorn

import settings


def main():
    uvicorn.run(
        "web.app:get_app",
        workers=settings.UVICORN_WORKERS,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.UVICORN_RELOAD,
        factory=True,
    )


if __name__ == "__main__":
    main()
