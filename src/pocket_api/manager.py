import os
import sys

from django.core.management import execute_from_command_line

from .config import settings


if __name__ == "__main__":

    os.environ["DJANGO_SETTINGS_MODULE"] = settings.__name__

    execute_from_command_line(sys.argv)
