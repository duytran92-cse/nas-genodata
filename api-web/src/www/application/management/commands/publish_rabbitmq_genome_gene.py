import json, pika, os
from application.models import *
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
import json
from application.modules.gene import components as gene_components
from django.db import connection


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
        GENOME_QUEUE = settings.GENOME_QUEUE
        RABBITMQ_HOST = settings.RABBITMQ_HOST
        RABBITMQ_PORT = int(settings.RABBITMQ_PORT)

        # Starting
        print "[x] Publish data to rabbitmq"
        ##########################
        ## Gene
        print "[***] Publish GENE data to rabbitmq"
        isDone = False
        start = 0
        gene_manager = gene_components.DataManager()
        while not isDone:
            end = start + 5000
            print 'start: %s, end: %s' % (start, end)
            gene = Gene.objects.all()[start:end]
            start = end + 1
            if gene.count() <= 0:
                isDone = True

            x = []
            for var in gene:
                y = ['gene', var.code]

                try:
                    data = gene_manager.get(var.code)
                    values = {}
                    arr_disease = []
                    asso_disease = []
                    asso_pub = []
                    for field, value in data.items():
                        if field in ['synonyms', 'effects','start', 'end','num_exon','chromosome','protein_product','description'] and value['value'] != None:
                            values[field] = value['value']
                        # disease field
                        if field == 'disgenet-diseases' and value['value'] != None:
                            arr_disease.extend(value['value'])
                            rs = [ item['disease'] for item in value['value'] ]
                            asso_disease.extend(rs)
                        if field == 'gwas-diseases' and value['value'] != None:
                            try:
                                for k in value['value']:
                                    arr_disease.append({
                                        'disease': k.get('disease',''),
                                        'pubmedid': k.get('pmid',''),
                                        'sentence': k.get('sentence', '')
                                    })
                            except Exception as e:
                                pass
                            rs = [ item['disease'] for item in value['value'] ]
                            asso_disease.extend(rs)
                        if field == 'ctdbase-diseases' and value['value'] != None:
                            try:
                                for k in value['value']:
                                    arr_disease.append({
                                        'disease': k.get('disease',''),
                                        'pubmedid': k.get('pmid',''),
                                        'sentence': k.get('evidence', '')
                                    })
                            except Exception as e:
                                pass

                            rs = [ item['disease'] for item in value['value'] ]
                            asso_disease.extend(rs)

                        if len(arr_disease) > 0:
                            values['disgenet-diseases'] = arr_disease
                        if len(asso_disease) > 0:
                            values['associated_diseases'] = asso_disease

                        # publications

                        if field == 'publications' and value['value'] != None:
                            values[field] = value['value']
                            try:
                                for k in value['value']:
                                    asso_pub.append({
                                        'pmid': k['pmid'],
                                        'title': k['title']
                                    })
                            except Exception as e:
                                pass
                        if field == 'gwas-publications' and value['value'] != None:
                            asso_pub.extend(value['value'])

                        if len(asso_pub) > 0:
                            values['associated_publications'] = asso_pub

                    if values:
                        y.append(values)
                        x.append(y)
                except Exception as e:
                    pass

            # Publish rabbitMQ
            self.publish_to_queue(x, GENOME_QUEUE, RABBITMQ_HOST, RABBITMQ_PORT)
        print "[***] DONE gene"

        print "[x] Sent data to RabbitMQ"
