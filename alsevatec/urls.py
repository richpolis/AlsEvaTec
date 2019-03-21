"""alsevatec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from albums.viewsets import AlbumViewSet, ArtistGroupViewSet
from services.views import random_text, service_soap
from .viewsets import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'artists', ArtistGroupViewSet)

urlpatterns = [
    url(r'^$', include('albums.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^random/text/', name='api_random_text', view=random_text),
    url(r'^service/soap/', name='api_service_soap', view=service_soap),
    url(r'^api-auth/', include('rest_framework.urls'))
]
