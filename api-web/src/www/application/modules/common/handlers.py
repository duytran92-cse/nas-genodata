from urad_api import registry
from urad_api_standard import handlers
from application.models import *
from . import components

class Summary(handlers.GetHandler):
    def get_record(self, params):
        data = {}
        obj = {
            'variation' : Variation.objects,
            'gene' : Gene.objects,
            'disease' : Disease.objects,
            'trait' : Trait.objects,
            'treatment' : Treatment.objects,
            'exon' : Exon.objects,
            'chromosome' : Chromosome.objects,
            'publication' : Publication.objects,
            'drug' : Drug.objects
        }

        for i in obj:
            data[i] = {
                'total': obj[i].all().count(),
                'total_of_good_quality': obj[i].filter(is_good_quality=True).count()
            }

        return data
