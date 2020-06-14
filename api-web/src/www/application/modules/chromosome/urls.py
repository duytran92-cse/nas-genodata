
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^list$',          handlers.List.as_view(),         name='chromosome_list'),
    url(r'^get$',           handlers.Get.as_view(),          name='chromosome_get'),
    url(r'^history$',       handlers.History.as_view(),      name='chromosome_history'),
    #url(r'^create$',        handlers.Create.as_view(),       name='chromosome_create'),
    #url(r'^update$',        handlers.Update.as_view(),       name='chromosome_update'),
    url(r'^delete$',        handlers.Delete.as_view(),       name='chromosome_delete'),
    url(r'^bulk_update$',   handlers.BulkUpdate.as_view(),   name='chromosome_bulk_update'),
    url(r'^list_detail$',   handlers.ListDetail.as_view(),   name='chromosome_list_detail'),
]
