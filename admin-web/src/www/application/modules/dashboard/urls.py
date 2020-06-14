
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                        actions.Dashboard.as_view(),     name='dashboard'),
]
