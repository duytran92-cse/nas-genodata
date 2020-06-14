import json, pika, os
from application.models import *
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
import json
from application.modules.variation import components as variation_components


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
        GENOME_QUEUE = 'genome-browser-variation'
        RABBITMQ_HOST = settings.RABBITMQ_HOST
        RABBITMQ_PORT = int(settings.RABBITMQ_PORT)

        # Starting
        print "[x] Publish data to rabbitmq"
        ##########################
        ## Variation
        isDone = False
        start = 0
        manager = variation_components.DataManager()
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
                    # print 'code: %s' % (code)
                    arr_disease = []
                    asso_disease = []
                    asso_pub = []
                    y['core_attributes'] = {
                        'chromosome': data['chromosome'].get('value', ''),
                        'position': data['vcf_RSPOS'].get('value', ''),
                        'allele_string': data['allele_string'].get('value', ''),
                        'synonyms': data['synonyms'].get('value', '')
                    }
                    y['genename'] = data['genename']['value']
                    y['1000-genomes'] = data['1000-genomes']['value']
                    if data['publications']['value']:
                        y['publications'] = data['publications']['value']
                    if data['gwas-effects']['value']:
                        y['effects'] = []
                        # y['effects'] = data['gwas-effects']['value']
                        for eff in data['gwas-effects']['value']:
                            effe = eff
                            if eff.get('effect', ''):
                                effe['risk'] = 'Increased risk of %s' % (eff['effect'])
                            else:
                                effe['risk'] = ''
                            if eff.get('initial', ''):
                                effe['evidences'] = 'Initial: %s' % (eff['initial'])
                                if eff.get('replication', ''):
                                    effe['evidences'] += ', replication: %s' % (eff['replication'])
                            else:
                                effe['evidences'] = ''
                            y['effects'].append(effe)
                    if data['genotype_frequency']['value']:
                        y['genotype_frequency'] = data['genotype_frequency']['value']

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
            print "[***] DONE variation"
