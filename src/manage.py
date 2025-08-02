import os
from fastapi_django.management import cli
from fastapi_django.management.utils import register_command

from commands.example_command import example_command


def main():
    os.environ.setdefault("FASTAPI_DJANGO_SETTINGS_MODULE", "settings")
    register_command(example_command)
    cli()

if __name__ == '__main__':
    main()
