import json, pika, os
from application.models import *
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
import json
from application.modules.variation import components


class Command(BaseCommand):
    ## PUBLISH
    def publish_to_queue(self, iterator, name_queue, rabbitmq_host, rabbitmq_port):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue=name_queue)
        for x in iterator:
            channel.basic_publish(exchange='', routing_key=name_queue, body=json.dumps(x))
        connection.close()


    def process(self, params = {}):
        # DECLARE VARIABLE
        NAME_QUEUE = 'user-variation'
        RABBITMQ_HOST = settings.RABBITMQ_HOST
        RABBITMQ_PORT = int(settings.RABBITMQ_PORT)

        # Starting
        print "[x] Publish data to rabbitmq"
        ##########################
        ## Variation
        isDone = False
        start = 0
        manager = components.DataManager()
        while not isDone:
            end = start + 5000
            variation = Variation.objects.filter(is_good_quality=True)[start:end]
            start = end + 1
            if variation.count() <= 0:
                isDone = True

            x = []
            for var in variation:
                y = {'version': '0.1', 'rsnumber': var.code}
                try:
                    data = manager.get(var.code)
                    arr_disease = []
                    y['chromosome'] = data['chromosome']['value']
                    y['position'] = data['vcf_RSPOS']['value']
                    y['science_filter'] = ''
                    y['genes'] = data['genename']['value']

                    if data['publications']['value']:
                        y['publications'] = data['publications']['value']
                    if data['gwas-effects']['value']:
                        y['effects'] = []
                        for eff in data['gwas-effects']['value']:
                            effe = {}
                            effe['genotype'] = eff['genotype']
                            effe['odd_ratio'] = eff['odd_ratio']
                            effe['effect'] = eff['effect']
                            y['effects'].append(effe)
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
                    if len(arr_disease) > 0:
                        y['diseases'] = arr_disease

                except Exception as e:
                    pass
                x.append(y)

            # Publish rabbitMQ
            self.publish_to_queue(x, NAME_QUEUE, RABBITMQ_HOST, RABBITMQ_PORT)
            print "[***] DONE variation"
