from __future__ import unicode_literals
from django.conf.urls import url, include
from rest_framework import routers

from . import views


urlpatterns = [

    url(r'^$',views.IndexView.as_view(template_name="albums/index.html"),name='albums-index'),
]
