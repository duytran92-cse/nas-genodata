import json
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from application.models import *
from application.modules.variation import components as variation_components

class Command(BaseCommand):
    def process(self, params = {}):
        fields = ['1000-genomes', 'allele_string','chromosome','genename','vcf_RSPOS']

        print '[***] Starting'
        # Reset this field
        Variation.objects.filter(is_good_quality=True).update(is_good_quality=False)

        variation_manager = variation_components.DataManager()
        isDone = False
        start = 0

        while not isDone:
            end = start + 5000
            # print 'start: %s, end: %s' % (start, end)
            records = Variation.objects.all()[start:end]
            start = end + 1
            if records.count() <= 0:
                isDone = True

            is_good_quality = False
            ids = []

            for var in records:
                count = 0
                data = variation_manager.get(var.code)
                for i in fields:
                    if i in data and data[i]['value'] != None:
                        count += 1
                if count == len(fields):
                    ids.append(var.id)

            # Update database
            Variation.objects.filter(pk__in=ids).update(is_good_quality=True)
            print '[***] %s is good quality ---- DONE' % (len(ids))
