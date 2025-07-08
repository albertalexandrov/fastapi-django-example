import os
import sys
from fastapi_django.management import cli


def main():
    os.environ.setdefault('FASTAPI_DJANGO_SETTINGS_MODULE', 'settings')
    cli(sys.argv)


if __name__ == '__main__':
    main()
