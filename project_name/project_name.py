import os
import sys

from django.conf import settings

DEBUG = os.environ.get('DEBUG','on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', '{{ secret_key }}')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOST','localhost').split(',')
settings.configure(

    SECRET_KEY=SECRET_KEY,
    DEBUG=DEBUG,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    MIDDLEWARE_CLASSES = [

        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
)

from django.http import HttpResponse
from django.urls import path
from django.core.wsgi import get_wsgi_application

def index(request):
    return HttpResponse("hello world")


urlpatterns = [
    path('',index,name='index'),
]


application = get_wsgi_application()


if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
