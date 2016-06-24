from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^indexation.html/?$', views.indexation),
    url(r'^home.html/?$', views.home),
]
