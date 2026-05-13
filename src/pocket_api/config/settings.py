import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
FILE_STORAGE_ROOT = os.environ.get(
    "POCKET_FILE_STORAGE_ROOT",
    os.path.join(BASE_DIR, "storage", "files"),
)

port = os.environ.get("DJANGO_PORT", 8080)
try:
    port = int(port)
except TypeError:
    raise TypeError(f"后端端口不是整数，端口为{port}")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "rest_framework",
    "pocket_api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pocket",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "123456",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": "pocket_api.result.result_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "pocket_api.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,  # 每页 10 条
}

DEBUG = True
ROOT_URLCONF = "pocket_api.config.urls"
PORT = port
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "*")
AUTH_USER_MODEL = "pocket_api.AdminUser"
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
MIGRATION_MODULES = {
    "admin": None,
    "auth": None,
    "contenttypes": None,
    "sessions": None,
}


ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
