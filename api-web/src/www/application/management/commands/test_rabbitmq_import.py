import json, pika, os
from urad_api import registry
from urad_api_standard.commands import Command as BaseCommand
from django.conf import settings
from application.modules.variation import components as variation_components
from application.modules.treatment import components as treatment_components
from application.modules.trait import components as trait_components
from application.modules.publication import components as publication_components
from application.modules.gene import components as gene_components
from application.modules.exon import components as exon_components
from application.modules.disease import components as disease_components
from application.modules.chromosome import components as chromosome_components
from application.modules.drug import components as drug_components


class Command(BaseCommand):
    _MANAGERS = {}
    def consume(self, ch, method, properties, body):
        data = json.loads(body)
        field_not_exist = []

        print "entity: %s, record: %s, field: %s, value: %s" % (data[1], data[2], data[3], data[4])
        if self._MANAGERS.get(data[1], None) !=  None:
            field_not_exist = self._MANAGERS[data[1]].put(data[2], {data[3]: data[4]}, source=data[0])
        if field_not_exist:
            print "[**] Fields are not exist in Genodata: %s" % (field_not_exist)

    def process(self, params = {}):
        self._MANAGERS = {
           'variation': variation_components.DataManager(),
           'treatment': treatment_components.DataManager(),
           'trait': trait_components.DataManager(),
           'publication': publication_components.DataManager(),
           'gene': gene_components.DataManager(),
           'exon': exon_components.DataManager(),
           'disease': disease_components.DataManager(),
           'chromosome': chromosome_components.DataManager(),
           'drug': drug_components.DataManager(),
        }
        print "[x] RECEIVING DATA"
        credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS)
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, '/', credentials))

        channel = connection.channel()
        channel.queue_declare(queue='test_queue', durable=True)

        print "[*] Waiting for data. To exit press CTRL+C"

        channel.basic_consume(self.consume, queue='test_queue', no_ack=True)
        channel.start_consuming()
