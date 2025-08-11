import os
from fastapi_django.management import typer


def main():
    os.environ.setdefault("FASTAPI_DJANGO_SETTINGS_MODULE", "settings")
    typer()

if __name__ == '__main__':
    main()
