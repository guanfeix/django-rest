import os
import sys
import hashlib

from django.conf import settings

DEBUG = os.environ.get('DEBUG','on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY',
                            'tusm0@1a&d+g%qr0zq4j0&a%1ry59pvt_*5au#21zc6f(7l&j#')


ALLOWED_HOSTS = ['*']
BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=True,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF='sitebuilder.urls',
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    MIDDLEWARE_CLASSES = [

        # 'django.middleware.common.CommonMiddleware',
        # 'django.middleware.csrf.CsrfViewMiddleware',
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS = [
        # 'django.contrib.admin',
        # 'django.contrib.auth',
        # 'django.contrib.contenttypes',
        # 'django.contrib.sessions',
        # 'django.contrib.messages',
        'django.contrib.staticfiles',
        'sitebuilder',
        'compressor',
        # 'polls',
    ],
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # 'DIRS': [os.path.join(BASE_DIR,"templates")],
            'DIRS': [],
            'APP_DIRS': True,
        },
    ],
    STATIC_URL = '/static/',
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR,"static"),
    # ],
    SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR, "pages"),
    SITE_OUTPUT_DIRECTORY=os.path.join(BASE_DIR, '_build'),
    STATIC_ROOT=os.path.join(BASE_DIR, '_build', 'static'),
    STATICFILES_FINDERS=(
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',),
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.CachedStaticFilesStorage'

)


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
