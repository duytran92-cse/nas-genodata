import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, chromosome):
        s = container.get_serializer()
        return {
            'id':                       chromosome['id'],
            'name':                     chromosome['name'],
            'synonyms':                 chromosome['synonyms'],
            'position':                 chromosome['position'],
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Chromosome, 'Chromosome')
        self.add_field('synonyms', 'list_string')
        self.add_field('start', 'string')
        self.add_field('end', 'string')
        # self.add_field('alias',' string')
