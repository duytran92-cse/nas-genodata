import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, variation):
        s = container.get_serializer()
        return {
            'id':                       variation['id'],
            'name':                     variation['name'],
            'synonyms':                 variation['synonyms'],
            'position':                 variation['position'],
            'is_somatic':               variation['is_somatic'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Publication, 'Publication')
        self.add_field('pmid', 'list_string')
        self.add_field('author', 'list_string')
        self.add_field('date', 'list_string')
        self.add_field('journal', 'list_string')
        self.add_field('title', 'list_string')
