import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, treatment):
        s = container.get_serializer()
        return {
            'id':                       treatment['id'],
            'name':                     treatment['name'],
            'synonyms':                 treatment['synonyms'],
            'position':                 treatment['position'],
            'is_somatic':               treatment['is_somatic'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Treatment, 'Treatment')
        self.add_field('synonyms', 'list_string','')
        self.add_field('publications', 'list_string','')
