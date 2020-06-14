from django.conf.urls import include, url
from application.modules.common import handlers

urlpatterns = [
    url(r'^variation/',                         include('application.modules.variation.urls')),
    url(r'^chromosome/',                        include('application.modules.chromosome.urls')),
    url(r'^disease/',                           include('application.modules.disease.urls')),
    url(r'^gene/',                              include('application.modules.gene.urls')),
    url(r'^trait/',                             include('application.modules.trait.urls')),
    url(r'^treatment/',                         include('application.modules.treatment.urls')),
    url(r'^publication/',                       include('application.modules.publication.urls')),
    url(r'^drug/',                              include('application.modules.drug.urls')),
    url(r'^accession/',                         include('application.modules.accession.urls')),
    url(r'^exon/',                              include('application.modules.exon.urls')),
    url(r'^summary',                            handlers.Summary.as_view(),         name='summary'),
]
