from django.conf import settings
from application.modules.common import page_contexts
import json
class PageStore(object):
    def __init__(self, container):
        self.container = container
    def list(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pageroffset'] = (page_number - 1) * 50
        params['_pagernum'] = 50
        params['_sortkey'] = sortkey
        params['_sortdir'] = sortdir
        if 'is_good_quality' not in params.keys():
            params['is_good_quality'] = True
        data = self.container.call_api(settings.GENODATA_API_URL + '/disease/list', GET=params)
        return data
    def get(self, id):
        return self.container.call_api(settings.GENODATA_API_URL + '/disease/get', GET={'id': id})
    def create(self, data):
        return self.container.call_api(settings.GENODATA_API_URL + '/disease/create', POST=data)
    def update(self, data, id):
        data['id'] = id
        return self.container.call_api(settings.GENODATA_API_URL + '/disease/update', POST=data)
    def history(self, id, field):
        return self.container.call_api(settings.GENODATA_API_URL + '/disease/history', GET={'id': id, 'field': field})
    def delete(self, id):
        return self.container.call_api(settings.GENODATA_API_URL + '/disease/delete', POST={'id': id})
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
        self.menu.set_group_selected('disease')
