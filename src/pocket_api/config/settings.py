import os

port = os.environ.get("DJANGO_PORT", 8080)
try:
    port = int(port)
except TypeError:
    raise TypeError(f"后端端口不是整数，端口为{port}")

DEBUG = True
ROOT_URLCONF = "pocket_api.config.urls"
PORT = port
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "*")
