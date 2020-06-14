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
    def serialize_record(self, treatment):
        return {
            'id':               treatment.id,
            'code':             treatment.code,
            'is_good_quality':  treatment.is_good_quality
        }

class Get(handlers.GetHandler):
    def get_record(self, params):
        manager = components.DataManager()
        code = Treatment.objects.get(pk=params['id'])
        treatment = manager.get(code.code)
        return treatment


class History(handlers.GetHandler):
    def get_record(self, params):
        manager = components.DataManager()
        treatment_history = manager.history(params['id'], params['field'])
        return treatment_history

class Delete(handlers.DeleteHandler):
    def POST(self, params):
        manager = components.DataManager()
        code = Treatment.objects.get(pk=params['id'])
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
    def serialize_record(self, treatment):
        manager = components.DataManager()
        fields = manager.get(treatment.code)
        data = {}
        for key, value in fields.items():
            if 'value' in value:
                data[key] = value['value']
        return {treatment.code: data}
