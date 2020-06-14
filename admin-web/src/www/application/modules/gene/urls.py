
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                    actions.List.as_view(),     name='gene_list'),
    # url(r'^create$',                  actions.Create.as_view(),   name='gene_create'),
    url(r'^delete/(?P<id>([a-zA-Z0-9- ]+))$', actions.Delete.as_view(),   name='gene_delete'),

    url(r'^update/(?P<code>([a-zA-Z0-9- ]+))$',   actions.Update.as_view(),   name='gene_update'),
    url(r'^history$',                    actions.History.as_view(),     name='gene_history'),
]
