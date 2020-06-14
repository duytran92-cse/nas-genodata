import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, drug):
        s = container.get_serializer()
        return {
            'id':                       drug['id'],
            'name':                     drug['name'],
            'synonyms':                 drug['synonyms'],
            'position':                 drug['position'],
            'is_somatic':               drug['is_somatic'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Drug, 'Drug')
        self.add_field('name', 'list_string','')
        self.add_field('source', 'list_string','')
        self.add_field('nested_parent', 'list_string','')
