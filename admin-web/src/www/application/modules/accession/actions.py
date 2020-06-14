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
            # html += '    <a class="btn btn-xs btn-primary" href="/accession/update/%s">Edit</a>' % (row['id'])
            html += '    <a class="btn btn-xs btn-danger" href="/accession/delete/%s" onclick="return confirm(\'Are you really want to delete this?\')">Delete</a>'  % (row['id'])
            html += '</div>'
            return html
    def create_table(self):
        table = widgets.table.DataTable()
        table.set_title('Accession')
        table.set_subtitle('List of accession')
        # table.create_button('create', '/accession/create', 'zmdi-plus')
        table.create_column('code', 'ID', '20%')
        table.create_column('chromosome', 'Chromosome', '20%')
        table.create_column('length', 'Length', '20%')
        table.create_column('reference_assembly', 'Reference assembly', '20%')
        table.create_column('actions', '', '14%')
        table.add_field(widgets.field.Textbox('text'))
        table.renderer = self.TableRenderer()
        table.renderer.table_form_renderer = renderers.widgets.form.TableFormRenderer()
        table.renderer.table_form_renderer.add_field('text', 'Search', colspan=8)
        table.renderer.table_form_renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return table
    def load_table_data(self, table_form_data, sortkey, sortdir, page_number):
        return components.PageStore(self.get_container()).list(table_form_data, sortkey, sortdir, page_number)

class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):

        form = widgets.form.Form()
        form.set_title('Accession')
        form.add_field(widgets.field.Textbox('code'))
        form.add_field(widgets.field.Textbox('chromosome'))
        form.add_field(widgets.field.Textbox('length'))
        form.add_field(widgets.field.Textbox('reference_assembly'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_field('code', 'Code')
        form.renderer.add_field('chromosome', 'Chromosome')
        form.renderer.add_field('length', 'Length')
        form.renderer.add_field('reference_assembly', 'Reference assembly')

        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        return form

    def load_form(self, form):
        result = components.PageStore(self.get_container()).get(self.params['id'])
        form.set_form_data(result)
    def process_form_data(self, data):
        return components.PageStore(self.get_container()).update(data, self.params['id'])


class Delete(actions.crud.DeleteAction):
    def GET(self):
        result = components.PageStore(self.get_container()).delete(self.params['id'])
        return HttpResponseRedirect('/accession/list')
