from django.urls import path, re_path
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    re_path(r'^(?P<slug>[\w./-]+)/$', page, name='page'),
    path('', page, name='homepage'),
]