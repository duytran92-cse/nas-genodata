import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, exon):
        s = container.get_serializer()
        return {
            'id':                       exon['id'],
            'name':                     exon['name'],
            'synonyms':                 exon['synonyms'],
            'position':                 exon['position'],
            'is_somatic':               exon['is_somatic'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Exon, 'Exon')
        self.add_field('rank', 'list_string')
        self.add_field('end', 'string')
        self.add_field('start', 'string')
        self.add_field('chromosome', 'list_string')
        self.add_field('gene', 'list_string')
        self.add_field('id', 'string')
