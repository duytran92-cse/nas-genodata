from django.template import loader
from notasquare.urad_web.renderers import BaseRenderer

class PageUpdateRenderer(BaseRenderer):
    def __init__(self):
        super(PageUpdateRenderer, self).__init__()
        self.template = 'material/custom/update.html'
    def render(self, table):
        template = loader.get_template(self.template)
        context = {}
        context['fields'] = sorted(table.data.items())
        context['title'] = table.data['code']
        context['page_id'] = table.data['page_id']
        return template.render(context)

class HistoryRenderer(BaseRenderer):
    def __init__(self):
        super(HistoryRenderer, self).__init__()
        self.template = 'material/custom/history.html'
    def render(self, table):
        template = loader.get_template(self.template)
        context = {}
        context['fields'] = table['data']
        context['field'] = table['text']['field']
        context['code'] = table['text']['code']
        return template.render(context)
