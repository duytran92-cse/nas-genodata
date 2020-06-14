from urad_api.base import BaseContainer
from . import serializers
from . import parsers

class StandardContainer(BaseContainer):
    def __init__(self):
        self.serializer = None
        self.parser = None
    def build(self):
        pass
    def get_request(self):
        pass
    def get_logger(self):
        pass
    def get_parser(self):
        return parsers.Parser()
    def get_exception_handler(self):
        pass
    def get_authorizator(self):
        pass
    def get_cache(self):
        pass
    def get_serializer(self):
        if self.serializer == None:
            self.serializer = serializers.Serializer()
        return self.serializer
