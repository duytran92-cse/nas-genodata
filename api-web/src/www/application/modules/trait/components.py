import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, trait):
        s = container.get_serializer()
        return {
            'id':                       trait['id'],
            'name':                     trait['name'],
            'synonyms':                 trait['synonyms'],
            'position':                 trait['position'],
            'is_somatic':               trait['is_somatic'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Trait, 'Trait')
        self.add_field('synonyms', 'list_string','')
        self.add_field('publications', 'list_string','')
