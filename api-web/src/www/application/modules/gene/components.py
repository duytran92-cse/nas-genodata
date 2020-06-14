import datetime, json
from urad_api.registry import container
from application import constants, models
from application.library import managers

class ModelSerializer(object):
    def serialize(self, gene):
        s = container.get_serializer()
        return {
            'id':               gene['id'],
            'name':             gene['name'],
            'description':      gene['description'],
            'position':         gene['position'],
            'is_reversed':      gene['is_reversed'],
            'biotype':          gene['biotype'],
            'havana_gene':      gene['havana_gene']
        }

class DataManager(managers.DataManager):
    def __init__(self):
        super(DataManager, self).__init__()
        self.set_key(models.Gene, 'Gene')
        self.add_field('geneid', 'list_string')
        self.add_field('chromosome', 'string')
        self.add_field('start', 'string')
        self.add_field('end', 'string')
        self.add_field('num_exon', 'string')
        self.add_field('protein_product', 'list_string')
        self.add_field('description', 'list_string')
        # self.add_field('associated_disease', 'list_string')
        self.add_field('synonyms', 'list_string')
        self.add_field('publications', 'list_string')
        self.add_field('havana_gene', 'list_string')
        self.add_field('biotype', 'list_string')
        self.add_field('is_reversed', 'boolean')
        self.add_field('ctdbase-diseases', 'list_string')
        self.add_field('disgenet-diseases', 'list_string')
        self.add_field('id', 'string')
        self.add_field('name', 'string')
        self.add_field('gwas-diseases', 'list_string', '')
        self.add_field('gwas-publications', 'list_string', '')
