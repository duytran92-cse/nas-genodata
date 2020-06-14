import json, pika, os
from application.models import *
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
import json
from application.modules.gene import components as gene_components


class Command(BaseCommand):
    ## PUBLISH
    def publish_to_queue(self, iterator, genome_queue, rabbitmq_host, rabbitmq_port):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue=genome_queue)
        for x in iterator:
            channel.basic_publish(exchange='', routing_key=genome_queue, body=json.dumps(x))
        connection.close()


    def process(self, params = {}):
        # DECLARE VARIABLE
        GENOME_QUEUE = 'genome-browser-gene'
        RABBITMQ_HOST = settings.RABBITMQ_HOST
        RABBITMQ_PORT = int(settings.RABBITMQ_PORT)

        # Starting
        print "[x] Publish data to rabbitmq"
        ##########################
        ## Variation
        isDone = False
        start = 0
        manager = gene_components.DataManager()
        while not isDone:
            end = start + 5000
            # print 'start: %s, end: %s' % (start, end)
            gene = Gene.objects.filter(is_good_quality=True)[start:end]
            start = end + 1
            if gene.count() <= 0:
                isDone = True

            x = []
            for var in gene:
                y = {'version': '0.1', 'name': var.code}
                try:
                    data = manager.get(var.code)
                    # print 'code: %s' % (code)
                    arr_disease = []
                    asso_disease = []
                    asso_pub = []
                    y['core_attributes'] = {
                        'chromosome': data['chromosome']['value'],
                        'start': data['start']['value'],
                        'end': data['end']['value'],
                        'synonyms': data['synonyms']['value'] if data['synonyms']['value'] != None else []
                    }
                    if data['publications']['value']:
                        y['publications'] = data['publications']['value']
                    if data['protein_product']['value']:
                        y['protein_product'] = data['protein_product']['value']
                    if data['description']['value']:
                        y['description'] = data['description']['value']
                    # disease
                    if data['disgenet-diseases']['value']:
                        arr_disease.extend(data['disgenet-diseases']['value'])
                        rs = [ item['disease'] for item in data['disgenet-diseases']['value'] ]
                        asso_disease.extend(rs)
                    if data['gwas-diseases']['value']:
                        for k in data['gwas-diseases']['value']:
                            arr_disease.append({
                                'disease': k.get('disease',''),
                                'pubmedid': k.get('pmid',''),
                                'sentence': k.get('sentence', '')
                            })
                        rs = [ item['disease'] for item in data['gwas-diseases']['value'] ]
                        asso_disease.extend(rs)
                    if data['ctdbase-diseases']['value']:
                        for k in data['gwas-diseases']['value']:
                            arr_disease.append({
                                'disease': k.get('disease',''),
                                'pubmedid': k.get('pmid',''),
                                'sentence': k.get('evidence', '')
                            })
                        rs = [ item['disease'] for item in data['gwas-diseases']['value'] ]
                        asso_disease.extend(rs)

                    if len(arr_disease) > 0:
                        y['disgenet-diseases'] = arr_disease
                    if len(asso_disease) > 0:
                        y['associated_diseases'] = asso_disease

                    # publication
                    if data['publications']['value']:
                        for k in data['publications']['value']:
                            asso_pub.append({
                                'pmid': k.get('pmid', ''),
                                'title': k.get('title','')
                            })
                    if data['gwas-publications']['value']:
                        asso_pub.extend(data['gwas-publications']['value'])
                    if len(asso_pub) > 0:
                        y['associated_publications'] = asso_pub

                except Exception as e:
                    pass
                x.append(y)
            # Publish rabbitMQ
            self.publish_to_queue(x, GENOME_QUEUE, RABBITMQ_HOST, RABBITMQ_PORT)
            print "[***] DONE gene"
