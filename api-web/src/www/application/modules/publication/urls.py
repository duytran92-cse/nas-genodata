
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^list$',          handlers.List.as_view(),         name='publication_list'),
    url(r'^get$',           handlers.Get.as_view(),          name='publication_get'),
    url(r'^history$',       handlers.History.as_view(),      name='publication_history'),
    #url(r'^create$',        handlers.Create.as_view(),       name='publication_create'),
    #url(r'^update$',        handlers.Update.as_view(),       name='publication_update'),
    url(r'^delete$',        handlers.Delete.as_view(),       name='publication_delete'),
    url(r'^bulk_update$',   handlers.BulkUpdate.as_view(),   name='publication_bulk_update'),
    url(r'^list_detail$',   handlers.ListDetail.as_view(),   name='publication_list_detail'),
]
