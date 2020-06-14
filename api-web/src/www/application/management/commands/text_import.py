import json, pika, os, gzip
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
from application.modules.variation import components as variation_components
from application.modules.treatment import components as treatment_components
from application.modules.trait import components as trait_components
from application.modules.publication import components as publication_components
from application.modules.gene import components as gene_components
from application.modules.exon import components as exon_components
from application.modules.disease import components as disease_components
from application.modules.chromosome import components as chromosome_components
from application.modules.drug import components as drug_components


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('_FILE', type=str, nargs='?', default='')

    def process(self, params = {}):
        _managers = {
            'variation': variation_components.DataManager(),
            'treatment': treatment_components.DataManager(),
            'trait': trait_components.DataManager(),
            'publication': publication_components.DataManager(),
            'gene': gene_components.DataManager(),
            'exon': exon_components.DataManager(),
            'disease': disease_components.DataManager(),
            'chromosome': chromosome_components.DataManager(),
            'drug': drug_components.DataManager(),
        }

        _filename = params.get('_FILE')
        if _filename:
            print "[x] RECEIVING DATA"
            try:
                with gzip.open('{}'.format(_filename), 'r') as f:
                    for line in f:
                        data = json.loads(line)
                        if len(data) >= 5:
                            field_not_exist = []
                            print "Entity: %s, Record: %s, Field: %s, Value: %s" % (data[1], data[2], data[3], data[4])
                            try:
                                if _managers.get(data[1], None) !=  None:
                                    field_not_exist = _managers[data[1]].put(data[2], {data[3]: data[4]}, source=data[0])
                            except Exception as e:
                                pass
                            if field_not_exist:
                                print "[**] Fields are not exist in Genodata: %s" % (field_not_exist)
            except Exception as e:
                raise e
        else:
            print "[Error] Expected gzip text file to import, empty given"
