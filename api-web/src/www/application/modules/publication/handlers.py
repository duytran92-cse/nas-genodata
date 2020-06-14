from urad_api import registry
from urad_api_standard import handlers
from application.models import *
from . import components


class List(handlers.ListHandler):
    def create_base_query(self, params):
        query = components.DataManager().model.objects
        if 'text' in params:
            query = query.filter(code__contains=params['text'])
        if 'is_good_quality' in params:
            if params['is_good_quality'] == 'True':
                query = query.filter(is_good_quality=True)
        return query
    def serialize_record(self, publication):
        return {
            'id':               publication.id,
            'code':             publication.code,
            'is_good_quality':  publication.is_good_quality
        }

class Get(handlers.GetHandler):
    def get_record(self, params):
        manager = components.DataManager()
        code = Publication.objects.get(pk=params['id'])
        publication = manager.get(code.code)
        return publication


class History(handlers.GetHandler):
    def get_record(self, params):
        manager = components.DataManager()
        publication_history = manager.history(params['id'], params['field'])
        return publication_history

class Delete(handlers.DeleteHandler):
    def POST(self, params):
        manager = components.DataManager()
        code = Publication.objects.get(pk=params['id'])
        manager.delete(code.code)
        return {}

class BulkUpdate(handlers.FormHandler):
    def POST(self, params):
        manager = components.DataManager()

        for item in data:
            source = item['source_id']
            for entry in item['entries']:
                manager.put(entry['record_code'], {entry['field_code']: entry['value']}, source=item['source_id'])

        return {}

class ListDetail(handlers.ListHandler):
    def create_base_query(self, params):
        query = components.DataManager().model.objects
        if 'text' in params:
            query = query.filter(code__contains=params['text'])
        return query
    def serialize_record(self, publication):
        manager = components.DataManager()
        fields = manager.get(publication.code)
        data = {}
        for key, value in fields.items():
            if 'value' in value:
                data[key] = value['value']
        return {publication.code: data}
