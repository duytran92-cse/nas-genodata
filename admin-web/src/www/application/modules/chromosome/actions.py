from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components

import json

class List(actions.crud.ListAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class TableRenderer(renderers.widgets.table.DataTableRenderer):
        def render_cell_actions(self, table, row):
            html  = '<div class="btn-group btn-group">'
            html += '    <a class="btn btn-xs btn-primary" href="/chromosome/update/%s">Edit</a>' % (row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/chromosome/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Chromosome')
        table.set_subtitle('List of chromosome')
        # table.create_button('create', '/chromosome/create', 'zmdi-plus')
        table.create_column('id', 'ID', '10%', sortable=True)
        table.create_column('code', 'Code', '60%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.add_field(widgets.field.Combobox('is_good_quality', choices=constants.FILTER))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Search', colspan=8)
        table.renderer.table_form_renderer.add_field('is_good_quality', 'Quality', colspan=4)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        table.renderer.table_form_renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.PageStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)


class Update(actions.crud.FormAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    class PageUpdateRenderer(renderers.page_update.PageUpdateRenderer):
        pass
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.PageUpdateRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).get(self.params['code'])
    def GET(self):
        page_context = self.create_page_context()
        table_widget = self.create_table()
        data = self.load_table_data()
        data['page_id'] = 'chromosome'
        table_widget.set_data(data)
        page_context.add_widget(table_widget)
        return HttpResponse(page_context.render())

class History(actions.crud.FormAction):
    class HistoryRenderer(renderers.page_update.HistoryRenderer):
        pass
    def create_table(self):
        table = widgets.table.DataTable()
        table.renderer = self.HistoryRenderer()
        return table
    def load_table_data(self):
        return components.PageStore(self.get_container()).history(self.params['code'], self.params['field'])
    def GET(self):
        page_context = renderers.page_update.HistoryRenderer()
        table_widget = self.create_table()
        record = self.load_table_data()
        data = {}
        data['data'] = record
        data['text'] = {'field': self.params['field'], 'code': self.params['code']}
        return HttpResponse(page_context.render(data))

class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.PageStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/chromosome/list')
