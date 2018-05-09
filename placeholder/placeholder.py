import os
import sys
import hashlib

from django.conf import settings

DEBUG = os.environ.get('DEBUG','on') == 'on'

SECRET_KEY = os.environ.get('SECRET_KEY',
                            'tusm0@1a&d+g%qr0zq4j0&a%1ry59pvt_*5au#21zc6f(7l&j#')

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOST','localhost').split(',')
ALLOWED_HOSTS = ['*']
BASE_DIR = os.path.dirname(__file__)

settings.configure(
    DEBUG=True,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    MIDDLEWARE_CLASSES = [

        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS = [
        # 'django.contrib.admin',
        # 'django.contrib.auth',
        # 'django.contrib.contenttypes',
        # 'django.contrib.sessions',
        # 'django.contrib.messages',
        'django.contrib.staticfiles',
        # 'polls',
    ],
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR,"templates")],
        },
    ],
    STATIC_URL = '/static/',
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR,"static"),
    ],
)

from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.http import etag
from django.core.wsgi import get_wsgi_application
from django.core.cache import cache
from django.urls import path, re_path, reverse
from django import forms
from django.shortcuts import render

from io import BytesIO
from PIL import Image,ImageDraw




class ImageForm(forms.Form):
    # 使用form表单来验证图片尺寸
    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    # 图像处理返回图片

    def generate(self, image_format='PNG'):
        height = self.cleaned_data["height"]
        width = self.cleaned_data["width"]
        # 2.引入缓存,key只是个字符串构造的键，用于取出我们村的值，这个不是啥问题
        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content is None:
            image = Image.new('RGB', (width, height))
            # 1.imagedraw加入文字
            draw = ImageDraw.Draw(image)
            text = '{} X {}'.format(width,height)
            textwidth, texthight = draw.textsize(text)
            if textwidth < width and texthight < height:
                texttop = (height - texthight) //2
                textleft = (width - textwidth) //2
                draw.text((textleft,texttop),text ,fill=(255,255,255))
            content = BytesIO()
            image.save(content,image_format)
            content.seek(0)
            cache.set(key, content, 60*60)
        return content


def generate_etag(request, width, height):
    content = 'Placeholder:{0} x {1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(generate_etag)
def placeholder(request, width, height ):
    form = ImageForm({"height": height, "width": width})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest("Invalid Image Request")


def index(request):
    example = reverse('placeholder',kwargs={'width':50, 'height':50})
    context = {
        'example': request.build_absolute_uri(example)
    }
    print(context,'--',example)
    return render(request, 'home.html', context)



urlpatterns = [
    path('', index,name='index'),
    re_path(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)',placeholder,name='placeholder'),
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
