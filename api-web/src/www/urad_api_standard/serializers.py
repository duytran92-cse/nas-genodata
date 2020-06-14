from urad_api.base import BaseSerializer

class Serializer(BaseSerializer):
    def serialize_date(self, data):
        if data == None:
            return ''
        return data.strftime('%Y-%m-%d')
    def serialize_datetime(self, data):
        if data == None:
            return ''
        return data.strftime('%Y-%m-%d %H:%M:%S')
    def serialize_boolean(self, data):
        return data
    def serialize_foreign_field(self, data, model):
        return {
            'id': data.id,        # Fix me: check how many query been called
            'label': data.name    # Fix me: generalize this
        }
    def serialize_many_to_many_field(self, data, model):
        records = []
        for r in data.all():
            records.append({
                'id':       r.id,     # Fix me: check how many query been called
                'label':    r.name    # Fix me: generalize this
            })
        return records
    def serialize_choice(self, data, choices):
        for c in choices:
            if c[0] == data:
                return {
                    'id': c[0],
                    'label': c[1]
                }
        return {'id': 0, 'label': ''}
