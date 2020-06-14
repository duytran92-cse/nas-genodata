from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from notasquare.urad_web import actions, page_contexts, widgets
from notasquare.urad_web_material import renderers
from application import constants
from . import components
from application.modules.page import components as page_components

class Update(actions.crud.UpdateAction):
    def create_page_context(self):
        return components.FullPageContext(self.params, self.container)
    def create_form(self):        
        pages = page_components.PageStore(self.get_container()).populate_combobox(kind='page')

        form = widgets.form.Form()
        form.set_title('Application setting')
        form.add_field(widgets.field.Textbox('application_title'))
        form.add_field(widgets.field.Textarea('contact_address_text'))
        form.add_field(widgets.field.Textarea('about_genopedia_text'))
        form.add_field(widgets.field.Textbox('facebook_url'))
        form.add_field(widgets.field.Textbox('twitter_url'))
        form.add_field(widgets.field.Textbox('youtube_url'))
        form.add_field(widgets.field.Textbox('linkedin_url'))
        form.add_field(widgets.field.Textbox('google_plus_url'))
        form.add_field(widgets.field.Combobox('impression_page', choices=pages, blank=True))
        form.add_field(widgets.field.Combobox('privacy_page', choices=pages, blank=True))
        form.add_field(widgets.field.Combobox('copyright_page', choices=pages, blank=True))
        form.add_field(widgets.field.Combobox('term_of_use_page', choices=pages, blank=True))
        form.add_field(widgets.field.Textbox('stat_num_variation'))
        form.add_field(widgets.field.Textbox('stat_num_gene'))
        form.add_field(widgets.field.Textbox('stat_num_disease'))
        form.add_field(widgets.field.Textbox('stat_num_disease_causing_mutation'))
        form.add_field(widgets.field.Textbox('stat_num_trait'))
        form.add_field(widgets.field.Textbox('stat_num_drug'))
        form.add_field(widgets.field.Textbox('stat_num_treatment'))
        form.add_field(widgets.field.Textbox('stat_num_cited_publication'))
        form.add_field(widgets.field.Textbox('stat_num_page'))
        form.add_field(widgets.field.Textbox('stat_num_registered_user'))
        form.add_field(widgets.field.Textbox('stat_num_genetic_code_letter'))
        form.add_field(widgets.field.Textbox('stat_num_forum_post'))
        form.renderer = renderers.widgets.form.HorizontalFormRenderer()
        form.renderer.add_section('Page information')
        form.renderer.add_field('application_title', 'Application title')
        form.renderer.add_field('contact_address_text', 'Contact address', rows=8)
        form.renderer.add_field('about_genopedia_text', 'About genopedia', rows=8)
        form.renderer.add_section('Social Networks')
        form.renderer.add_field('facebook_url', 'Facebook')
        form.renderer.add_field('twitter_url', 'Twitter')
        form.renderer.add_field('youtube_url', 'Youtube')
        form.renderer.add_field('linkedin_url', 'LinkedIn')
        form.renderer.add_field('google_plus_url', 'Google Plus')
        form.renderer.add_section('Pages')
        form.renderer.add_field('impression_page', 'Impression')
        form.renderer.add_field('privacy_page', 'Privacy')
        form.renderer.add_field('copyright_page', 'Copyright')
        form.renderer.add_field('term_of_use_page', 'Term of use')
        form.renderer.add_section('Statistics')
        form.renderer.add_field('stat_num_variation', 'Num variations')
        form.renderer.add_field('stat_num_gene', 'Num genes')
        form.renderer.add_field('stat_num_disease', 'Num diseases')
        form.renderer.add_field('stat_num_disease_causing_mutation', 'Num diseases causing mutations')
        form.renderer.add_field('stat_num_trait', 'Num traits')
        form.renderer.add_field('stat_num_drug', 'Num drug')
        form.renderer.add_field('stat_num_treatment', 'Num treatment')
        form.renderer.add_field('stat_num_cited_publication', 'Num cited publication')
        form.renderer.add_field('stat_num_page', 'Num pages')
        form.renderer.add_field('stat_num_registered_user', 'Num registered users')
        form.renderer.add_field('stat_num_genetic_code_letter', 'Num genetic code letters')
        form.renderer.add_field('stat_num_forum_post', 'Num forum posts')
        form.renderer.set_field_renderer('textbox', renderers.widgets.field.TextboxRenderer())
        form.renderer.set_field_renderer('textarea', renderers.widgets.field.TextareaRenderer())
        form.renderer.set_field_renderer('combobox', renderers.widgets.field.ComboboxRenderer())
        return form
    def load_form(self, form):
        result = components.ApplicationSettingStore(self.get_container()).get()
        if result['status'] == 'ok':
            record = result['data']['record']
            form.set_form_data(record)
        else:
            form.add_message('danger', "Can't load form")
    def process_form_data(self, data):
        return components.ApplicationSettingStore(self.get_container()).update(data)
