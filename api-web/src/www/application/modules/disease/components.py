import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, disease):
        s = container.get_serializer()
        return {
            'id':                       disease['id'],
            'name':                     disease['name'],
            'synonyms':                 disease['synonyms'],
            'position':                 disease['position'],
            'is_somatic':               disease['is_somatic'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Disease, 'Disease')
        self.add_field('synonyms', 'list_string')
        self.add_field('associated_gene', 'list_string')
        self.add_field('associated_publications', 'list_string')
        self.add_field('publications', 'list_string')
