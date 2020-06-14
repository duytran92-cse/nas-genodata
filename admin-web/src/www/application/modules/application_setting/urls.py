
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^update$',  actions.Update.as_view(),   name='application_setting_update'),
]
