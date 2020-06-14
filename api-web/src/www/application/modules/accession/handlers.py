from urad_api import registry
from urad_api_standard import handlers
from application.models import *


class List(handlers.ListHandler):
    def create_base_query(self, params):
        query = Accession.objects
        if 'text' in params:
            query = query.filter(code__contains=params['text'])
        return query
    def serialize_record(self, accession):
        return {
            'id':                   accession.id,
            'code':                 accession.code,
            'reference_assembly':   accession.reference_assembly,
            'chromosome':           accession.chromosome,
            'length':               accession.length
        }

class Get(handlers.GetHandler):
    def get_record(self, params):
        accession = Accession.objects.get(pk=params['id'])
        return {
            'id':                   accession.id,
            'code':                 accession.code,
            'reference_assembly':   accession.reference_assembly,
            'chromosome':           accession.chromosome,
            'length':               accession.length
        }

class Delete(handlers.DeleteHandler):
    def POST(self, params):
        accession = Accession.objects.get(pk=params['id'])
        accession.delete()
        return 1
