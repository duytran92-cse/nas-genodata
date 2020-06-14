import json, pika, os
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings

class Command(BaseCommand):
    def process(self, params = {}):
        print "Publish data to rabbitmq"

        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        # data = ["gwas-1.0.1", "variation", "rs1658442", "effects", [{"initial": "22,100 European ancestry individuals", "odd_ratio": "", "title": "Identification of a candidate gene for astigmatism.", "risk_allele": "A", "journal": "Invest Ophthalmol Vis Sci", "author": "Lopes MC", "mapped_trait": "Astigmatism", "effect": "Corneal astigmatism", "replication": "", "date": "2013-01-15", "risk_allele_frequency": "", "pmid": "23322567", "population": ["Global"]}, {"initial": "22,100 European ancestry individuals", "odd_ratio": "", "title": "Identification of a candidate gene for astigmatism.", "risk_allele": "A", "journal": "Invest Ophthalmol Vis Sci", "author": "Lopes MC", "mapped_trait": "Astigmatism", "effect": "Corneal astigmatism", "replication": "", "date": "2013-01-15", "risk_allele_frequency": "", "pmid": "23322567", "population": ["Global"]}]]
        data = ["gwas-1.0.1", "variation", "rs123456", "synonyms", [{"effect": "Corneal astigmatism", "population": ["Global"]}]]
        channel.queue_declare(queue='test_queue', durable=True)
        message = json.dumps(data)
        channel.basic_publish(exchange='',
                              routing_key='test_queue',
                              body='fsdfsd')
        print(" [x] Sent data to RabbitMQ")
        connection.close()
