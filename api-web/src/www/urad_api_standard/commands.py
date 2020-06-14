from urad_api.base import BaseCommand
from django.utils.module_loading import import_string
from django.conf import settings
from urad_api import registry

class Command(BaseCommand):
    def bootstrap(self):
        kclass = import_string(settings.URAD_API_COMMAND_CONTAINER)
        registry.container = kclass()
        registry.container.build()
    def process(self, params = {}):
        pass
    def handle(self, *args, **options):
        self.bootstrap()
        params = options
        self.process(params)
