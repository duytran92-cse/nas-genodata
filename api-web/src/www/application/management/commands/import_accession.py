import json
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from application.models import *

class Command(BaseCommand):
    def process(self, params = {}):
        print "Import data for accession"
        records = [
                    {"id":"NC_000001.10","chromosome":"1","length":249250621},
                    {"id":"NC_000002.11","chromosome":"2","length":243199373},
                    {"id":"NC_000003.11","chromosome":"3","length":198022430},
                    {"id":"NC_000004.11","chromosome":"4","length":191154276},
                    {"id":"NC_000005.9","chromosome":"5","length":180915260},
                    {"id":"NC_000006.11","chromosome":"6","length":171115067},
                    {"id":"NC_000007.13","chromosome":"7","length":159138663},
                    {"id":"NC_000008.10","chromosome":"8","length":146364022},
                    {"id":"NC_000009.11","chromosome":"9","length":141213431},
                    {"id":"NC_000010.10","chromosome":"10","length":135534747},
                    {"id":"NC_000011.9","chromosome":"11","length":135006516},
                    {"id":"NC_000012.11","chromosome":"12","length":133851895},
                    {"id":"NC_000013.10","chromosome":"13","length":115169878},
                    {"id":"NC_000014.8","chromosome":"14","length":107349540},
                    {"id":"NC_000015.9","chromosome":"15","length":102531392},
                    {"id":"NC_000016.9","chromosome":"16","length":90354753},
                    {"id":"NC_000017.10","chromosome":"17","length":81195210},
                    {"id":"NC_000018.9","chromosome":"18","length":78077248},
                    {"id":"NC_000019.9","chromosome":"19","length":59128983},
                    {"id":"NC_000020.10","chromosome":"20","length":63025520},
                    {"id":"NC_000021.8","chromosome":"21","length":48129895},
                    {"id":"NC_000022.10","chromosome":"22","length":51304566},
                    {"id":"NC_000023.10","chromosome":"X","length":155270560},
                    {"id":"NC_000024.9","chromosome":"Y","length":59373566},
                    {"id":"NC_012920.1","chromosome":"MT","length":16569}
                  ]
        accessions = []
        reference_assembly = 'NCBI build 37'
        for item in records:
            accession = Accession()
            accession.code = item['id']
            accession.chromosome = item['chromosome']
            accession.length = item['length']
            accession.reference_assembly = reference_assembly
            accessions.append(accession)
        Accession.objects.bulk_create(accessions)
        print "Done"
