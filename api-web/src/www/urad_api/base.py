import json, traceback
from django.views.generic.base import View
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.module_loading import import_string
from django.test import TestCase, Client
from django.core.management.base import BaseCommand
from . import registry

class BaseContainer(object):
    def __init__(self):
        pass
    def build(self):
        pass
    def get_request(self):
        pass
    def get_logger(self):
        pass
    def get_parser(self):
        pass
    def get_exception_handler(self):
        pass
    def get_authorizator(self):
        pass
    def get_cache(self):
        pass
    def get_serializer(self):
        pass

class BaseRequestParser(object):
    def parse(self, request, **kwargs):
        pass

class BaseExceptionHandler(object):
    def response(self, exception):
        pass

class BaseParser(object):
    pass

class BaseUnitTest(TestCase):
    def init(self):
        self.client = Client()
        self.headers = {}
        kclass = import_string(settings.URAD_API_UNIT_TEST_CONTAINER)
        registry.container = kclass()
        registry.container.build()

class BaseSerializer(object):
    pass

class BaseCommand(BaseCommand):
    pass

class BaseHandler(View):
    def __init__(self):
        self.container = None
    def bootstrap(self, request):
        kclass = import_string(settings.URAD_API_HANDLER_CONTAINER)
        registry.container = kclass()
        registry.container.build()
    def merge_params(self, request, **kwargs):
        params = {}
        for k in request.GET.iterkeys():
            params[k] = request.GET.get(k)

        if request.body != '':
            req = json.loads(request.body)
            for k in req:
                params[k] = req[k]

        for k in kwargs:
            params[k] = kwargs[k]
        return params
    def response_exception(self, exception):
        traceback.print_exc(exception)
        return HttpResponse(status=500)

    # GET
    def GET(self, parameters):
        return {}
    def get(self, request, **kwargs):
        try:
            self.bootstrap(request)
            parameters = self.merge_params(request, **kwargs)
            return JsonResponse(self.GET(parameters), safe=False)
        except Exception as e:
            return self.response_exception(e)

    # POST
    def POST(self, parameters):
        return {}
    def post(self, request, **kwargs):
        try:
            self.bootstrap(request)
            parameters = self.merge_params(request, **kwargs)
            return JsonResponse(self.POST(parameters))
        except Exception as e:
            return self.response_exception(e)
