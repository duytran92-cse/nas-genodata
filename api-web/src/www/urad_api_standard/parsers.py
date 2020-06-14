import datetime
from urad_api.base import BaseParser
from django.apps import apps

class Parser(BaseParser):
    def __init__(self):
        self.params = {}
        self.errors = {}
    def set_params(self, params):
        self.params = params
        self.errors = {}
    def get_errors(self):
        return self.errors
    def has_error(self):
        return len(self.errors) > 0

    # Utility
    def is_set(self, key):
        return key in self.params
    def get(self, key):
        return self.params[key]

    # Validators
    def validate_not_empty(self, key):
        is_empty = True
        if key in self.params:
            if self.params[key]:
                is_empty = False
            else:
                is_empty = True
        if is_empty:
            self.errors[key] = 'VALIDATE_NOT_EMPTY'
        return not is_empty

    # Parser
    def parse_text(self, key):
        return self.params[key]
    def parse_boolean(self, key):
        return self.params[key]
    def parse_date(self, key):
        return datetime.datetime.strptime(self.params[key], '%Y-%m-%d')
    def parse_datetime(self, key):
        return datetime.datetime.strptime(self.params[key], '%Y-%m-%d %H:%M:%S')
    def parse_model(self, key, model):
        if isinstance(model, basestring):
            model = apps.get_model(model)
        return model.objects.get(pk=self.params[key])
    def parse_choice(self, key, choices):
        for c in choices:
            if self.params[key] == c[0]:
                return c[0]
        return ''
    def parse_int_list(self, key):
        return self.params[key]
