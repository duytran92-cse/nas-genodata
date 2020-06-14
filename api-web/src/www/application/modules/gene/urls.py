
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^list$',          handlers.List.as_view(),         name='gene_list'),
    url(r'^get$',           handlers.Get.as_view(),          name='gene_get'),
    url(r'^history$',       handlers.History.as_view(),      name='gene_history'),
    #url(r'^create$',        handlers.Create.as_view(),       name='gene_create'),
    #url(r'^update$',        handlers.Update.as_view(),       name='gene_update'),
    url(r'^delete$',        handlers.Delete.as_view(),       name='gene_delete'),
    url(r'^bulk_update$',   handlers.BulkUpdate.as_view(),   name='gene_bulk_update'),
    url(r'^list_detail$',   handlers.ListDetail.as_view(),   name='gene_list_detail'),
]
