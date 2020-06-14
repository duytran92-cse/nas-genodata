import json, pika, os
from application.models import *
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
import json
from application.modules.variation import components as variation_components


class Command(BaseCommand):
    ## PUBLISH
    def publish_to_queue(self, iterator, sequence_queue, rabbitmq_host, rabbitmq_port):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue=sequence_queue)
        for x in iterator:
            channel.basic_publish(exchange='', routing_key=sequence_queue, body=json.dumps(x))
        connection.close()

    def process(self, params = {}):
        # DECLARE VARIABLE
        SEQUENCE_QUEUE = 'sequence-viewer-variation'
        RABBITMQ_HOST = settings.RABBITMQ_HOST
        RABBITMQ_PORT = int(settings.RABBITMQ_PORT)

        # Starting
        print "[x] Publish data to rabbitmq"

        ##########################
        ## Variation
        isDone = False
        start = 0
        variation_manager = variation_components.DataManager()
        fields = ['chromosome', 'genename', 'vcf_RSPOS']

        while not isDone:
            end = start + 5000

            variation = Variation.objects.all()[start:end]
            start = end + 1
            if variation.count() <= 0:
                isDone = True
            x = []

            for var in variation:
                count = 0
                y = ['variation', var.code]
                arr_disease = []
                data = variation_manager.get(var.code)
                for i in fields:
                    if i in data and data[i]['value'] != None:
                        count += 1
                if count == len(fields):
                    # disease
                    if data['disgenet-diseases']['value']:
                        arr_disease.extend(data['disgenet-diseases']['value'])
                    if data['gwas-diseases']['value']:
                        for k in data['gwas-diseases']['value']:
                            arr_disease.append({
                                'disease': k.get('disease',''),
                                'pubmedid': k.get('pmid',''),
                                'sentence': k.get('sentence', '')
                            })

                    y.append({
                        'chromosome': data['chromosome']['value'],
                        'genename': data['genename']['value'],
                        'position': data['vcf_RSPOS']['value'],
                        'associated_diseases': arr_disease
                    })
                    x.append(y)

            if len(x) > 0:
                print "[***] starting publish to rabbitMQ"
                # Publish rabbitMQ
                self.publish_to_queue(x, SEQUENCE_QUEUE, RABBITMQ_HOST, RABBITMQ_PORT)
        print "[***] DONE variation"
