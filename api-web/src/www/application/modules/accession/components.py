import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, accession):
        s = container.get_serializer()
        return {
            'id':                       accession['id'],
            'name':                     accession['name'],
            'synonyms':                 accession['synonyms'],
            'position':                 accession['position'],
            'is_somatic':               accession['is_somatic'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Accession, 'Accession')
        self.add_field('chromosome', 'list_string','')
        self.add_field('length', 'integer','')
