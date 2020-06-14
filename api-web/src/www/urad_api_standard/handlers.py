from urad_api.base import BaseHandler
from urad_api.registry import container
from django.forms.models import model_to_dict


class GetHandler(BaseHandler):
    def parse_and_validate(self, params):
        return params
    def get_record(self, params):
        return {}
    def GET(self, params):
        params = self.parse_and_validate(params)
        return self.get_record(params)


class ListHandler(BaseHandler):
    def __init__(self):
        super(ListHandler, self).__init__()
    def parse_and_validate(self, params):
        return params
    def extract_sort_params(self, params):
        sortkey = params['_sortkey'] if '_sortkey' in params else None
        sortdir = params['_sortdir'] if '_sortdir' in params else 'asc'
        return (sortkey, sortdir)
    def extract_pager_params(self, params):
        pageroffset = int(params['_pageroffset']) if '_pageroffset' in params else 0
        pagernum = int(params['_pagernum']) if '_pagernum' in params else 100
        return (pageroffset, pagernum)
    def create_base_query(self, params):
        pass
    def build_sort_query(self, query, sortkey, sortdir):
        if sortkey == None:
            return query
        key = sortkey
        if sortdir == 'desc':
            key = '-' + key
        query = query.order_by(key)
        return query
    def serialize_record(self, record):
        return model_to_dict(record)
    def get_data(self, filters={}, sortkey = None, sortdir='asc', pageroffset=0, pagernum=100):
        query = self.create_base_query(filters)
        query = self.build_sort_query(query, sortkey, sortdir)
        records = []
        start = pageroffset
        end = pageroffset + pagernum
        for r in query.all()[start:end]:
            records.append(self.serialize_record(r))
        query = self.create_base_query(filters)
        total_matched = query.count()
        return (records, total_matched)
    def GET(self, params):
        params = self.parse_and_validate(params)
        (sortkey, sortdir) = self.extract_sort_params(params)
        (pageroffset, pagernum) = self.extract_pager_params(params)
        (records, total_matched) = self.get_data(params, sortkey, sortdir, pageroffset, pagernum)
        return {
            'records':       records,
            'total_matched': total_matched
        }


class FormHandler(BaseHandler):
    pass

class DeleteHandler(BaseHandler):
    def POST(self, params):
        return {}
