from django.conf import settings

class ApplicationSettingStore(object):
    def __init__(self, container):
        self.container = container
    def get(self):
        return self.container.call_api(settings.GENODATA_API_URL + '/application_setting/get', GET={})
    def update(self, data):
        return self.container.call_api(settings.GENODATA_API_URL + '/application_setting/update', POST=data)

class FullPageContext(page_contexts.FullPageContext):
    def __init__(self, params,container):
        super(FullPageContext, self).__init__(container.request)
        self.menu.set_group_selected('application_setting')
