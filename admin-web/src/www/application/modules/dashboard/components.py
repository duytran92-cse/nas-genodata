from django.conf import settings
from application.modules.common import page_contexts
import json
class PageStore(object):
    def __init__(self, container):
        self.container = container
    def summary(self, params={}, sortkey='id', sortdir='desc', page_number=1):
        params['_pager_start'] = (page_number - 1) * 10
        params['_pager_num'] = 10
        params['_sort_key'] = sortkey
        params['_sort_dir'] = sortdir
        data = self.container.call_api(settings.GENODATA_API_URL + '/summary')
        return data

class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params,container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('dashboard')
