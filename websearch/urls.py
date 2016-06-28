from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^indexation/?$', views.indexation),
    url(r'^urls/?$', views.urls),
    url(r'^settings/?$', views.settings)
]
