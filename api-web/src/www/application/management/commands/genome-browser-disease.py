import json, pika, os
from application.models import *
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
import json
from application.modules.disease import components as disease_components


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
        GENOME_QUEUE = 'genome-browser-disease'
        RABBITMQ_HOST = settings.RABBITMQ_HOST
        RABBITMQ_PORT = int(settings.RABBITMQ_PORT)

        # Starting
        print "[x] Publish data to rabbitmq"
        ##########################
        ## Variation
        isDone = False
        start = 0
        manager = disease_components.DataManager()
        while not isDone:
            end = start + 5000
            disease = Disease.objects.filter(is_good_quality=True)[start:end]
            start = end + 1
            if disease.count() <= 0:
                isDone = True

            x = []
            for var in disease:
                y = {'version': '0.1', 'name': var.code}
                try:
                    data = manager.get(var.code)
                    # print 'code: %s' % (code)
                    asso_pub = []
                    y['core_attributes'] = {
                        'synonyms': data['synonyms']['value'] if data['synonyms']['value'] != None else []
                    }
                    if data['associated_gene']['value']:
                        y['associated_gene'] = data['associated_gene']['value']
                    if data['publications']['value']:
                        y['publications'] = data['publications']['value']

                    # publication
                    if data['publications']['value']:
                        for k in data['publications']['value']:
                            asso_pub.append({
                                'pmid': k.get('pmid', ''),
                                'title': k.get('title','')
                            })
                    if len(asso_pub) > 0:
                        y['associated_publications'] = asso_pub

                except Exception as e:
                    pass
                x.append(y)

            # Publish rabbitMQ
            self.publish_to_queue(x, GENOME_QUEUE, RABBITMQ_HOST, RABBITMQ_PORT)
            print "[***] DONE disease"
