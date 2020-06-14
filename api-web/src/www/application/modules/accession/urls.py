
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^list$',          handlers.List.as_view(),         name='accession_list'),
    url(r'^get$',           handlers.Get.as_view(),          name='accession_get'),
    #url(r'^create$',        handlers.Create.as_view(),       name='accession_create'),
    # url(r'^update$',        handlers.Update.as_view(),       name='accession_update'),
    url(r'^delete$',        handlers.Delete.as_view(),       name='accession_delete')
]
