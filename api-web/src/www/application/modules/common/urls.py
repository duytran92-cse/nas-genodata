
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^summary$',              handlers.Summary.as_view(),                name='summary'),
]
