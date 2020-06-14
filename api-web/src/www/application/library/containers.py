import voldemort
from django.conf import settings
from urad_api_standard import containers
# from . import genodb

class Container(containers.StandardContainer):
    def get_voldemort_client(self):
        if not hasattr(self, 'voldemort_client'):
            self.voldemort_client = voldemort.StoreClient(settings.VOLDEMORT_DATABASE_NAME, settings.VOLDEMORT_NODES)
        return self.voldemort_client
