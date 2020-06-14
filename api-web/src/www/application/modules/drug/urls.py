
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^list$',          handlers.List.as_view(),         name='drug_list'),
    url(r'^get$',           handlers.Get.as_view(),          name='drug_get'),
    url(r'^history$',       handlers.History.as_view(),      name='drug_history'),
    #url(r'^create$',        handlers.Create.as_view(),       name='drug_create'),
    #url(r'^update$',        handlers.Update.as_view(),       name='drug_update'),
    url(r'^delete$',        handlers.Delete.as_view(),       name='drug_delete'),
    url(r'^bulk_update$',   handlers.BulkUpdate.as_view(),   name='drug_bulk_update'),
    url(r'^list_detail$',   handlers.ListDetail.as_view(),   name='drug_list_detail'),
]
