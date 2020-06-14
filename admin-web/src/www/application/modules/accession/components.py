from django.conf import settings
from application.modules.common import page_contexts
import json
class PageStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pageroffset'] = (page_number - 1) * 10
        params['_pagernum'] = 10
        params['_sortkey'] = sortkey
        params['_sortdir'] = sortdir
        data = self.container.call_api(settings.GENODATA_API_URL + '/accession/list', GET=params)
        return data
    def get(self, id):
        a = self.container.call_api(settings.GENODATA_API_URL + '/accession/get', GET={'id': id})
        return a
    def create(self, data):
        return self.container.call_api(settings.GENODATA_API_URL + '/accession/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENODATA_API_URL + '/accession/update', POST=data)
    def delete(self, id):
        return self.container.call_api(settings.GENODATA_API_URL + '/accession/delete', POST={'id': id})
    def populate_combobox(self, kind=''):
        choices = []
        params = {}
        if kind != '':
            params['kind'] = kind
        records = self.list(sortkey='title', sortdir='asc', params=params)
        for record in records['records']:
            choices.append({
                'id':     record['id'],
                'label':  record['title']
            })
        return choices


class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params,container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('accession')
