import datetime, json
from urad_api import registry


class BaseSerializer(object):
    def serialize(self, value, params={}):
        return str(value)
    def deserialize(self, str, params={}):
        return str

class StringSerializer(BaseSerializer):
    def serialize(self, value, params={}):
        return str(value)
    def deserialize(self, str, params={}):
        return str

class ListStringSerializer(BaseSerializer):
    def serialize(self, value, params={}):
        return json.dumps(value)
    def deserialize(self, str, params={}):
        return json.loads(str)

class IntegerSerializer(BaseSerializer):
    def serialize(self, value, params={}):
        return str(value)
    def deserialize(self, str, params={}):
        return int(str)

class BooleanSerializer(BaseSerializer):
    def serialize(self, value, params={}):
        return "1" if value else "0"
    def deserialize(self, str, params={}):
        return str == "1"

class DataManager(object):
    def __init__(self):
        self.voldemort = registry.container.get_voldemort_client()
        self.model = None
        self.kvcode = '_'
        self.fields = {}
        self.serializers = {}
        self.add_serializer('string', StringSerializer())
        self.add_serializer('integer', IntegerSerializer())
        self.add_serializer('boolean', BooleanSerializer())
        self.add_serializer('list_string', ListStringSerializer())
    def set_key(self, model, kvcode):
        self.model = model
        self.kvcode = kvcode
    def add_serializer(self, datatype, serializer):
        self.serializers[datatype] = serializer
    def add_field(self, id, datatype, params = {}):
        self.fields[id] = {
            'datatype':    datatype,
            'params':      params
        }
    def _key(self, pk, field_id, tag, version=''):
        if version != '':
            return '%s?%s?%s?%s?%s' % (str(self.kvcode), str(pk), str(field_id), str(tag), str(version))
        return '%s?%s?%s?%s' % (str(self.kvcode), str(pk), str(field_id), str(tag))
    def _extract_key(self, key):
        tokens = key.split('?')
        pk = tokens[1]
        field_id = tokens[2]
        tag = tokens[3]
        version = int(tokens[4]) if len(tokens) >= 5 else ''
        return (pk, field_id, tag, version)
    def _get_serializer(self, datatype):
        return self.serializers[datatype]
    def _serialize(self, field_id, value):
        datatype = self.fields[field_id]['datatype']
        params = self.fields[field_id]['params']
        return self._get_serializer(datatype).serialize(value, params)
    def _deserialize(self, field_id, value):
        datatype = self.fields[field_id]['datatype']
        params = self.fields[field_id]['params']
        return self._get_serializer(datatype).deserialize(value, params)
    def get(self, pk):
        data = {}

        if self.model.objects.filter(code=pk).count() == 0:
            return None
        obj = self.model.objects.filter(code=pk).all()[0]
        data['code'] = obj.code

        keys = []
        for field_id in self.fields.iterkeys():
            keys.append(self._key(pk, field_id, 'value'))
            keys.append(self._key(pk, field_id, 'source'))
            keys.append(self._key(pk, field_id, 'timestamp'))
            keys.append(self._key(pk, field_id, 'version'))
            keys.append(self._key(pk, field_id, 'max_version'))
            data[field_id] = {
                'value':        None,
                'source':       None,
                'timestamp':    None,
                'version':      0,
                'max_version':  0,
                'params':       self.fields[field_id]['params']
            }
        records = self.voldemort.get_all(keys)
        for k in records.iterkeys():
            (pk, field_id, tag, version) = self._extract_key(k)
            data[field_id][tag] = records[k][0][0]
            if tag == 'value':
                data[field_id][tag] = self._deserialize(field_id, data[field_id][tag])
        return data
    def put(self, pk, data, source='_'):
        if self.model.objects.filter(code=pk).count() == 0:
            obj = self.model()
            obj.code = pk
            obj.save()

        keys = []
        field_max_version = {}
        for field_id in self.fields.iterkeys():
            keys.append(self._key(pk, field_id, 'max_version'))
            field_max_version[field_id] = 0
        records = self.voldemort.get_all(keys)
        for k in records.iterkeys():
            (pk, field_id, tag, version) = self._extract_key(k)
            field_max_version[field_id] = int(records[k][0][0])

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        field_not_exist = []
        for field_id in self.fields.iterkeys():
            if field_id in data:
                version = field_max_version[field_id] + 1
                value = data[field_id]
                value = self._serialize(field_id, value)

                self.voldemort.put(self._key(pk, field_id, 'value'),       str(value))
                self.voldemort.put(self._key(pk, field_id, 'source'),      str(source))
                self.voldemort.put(self._key(pk, field_id, 'timestamp'),   str(timestamp))
                self.voldemort.put(self._key(pk, field_id, 'version'),     str(version))
                self.voldemort.put(self._key(pk, field_id, 'max_version'), str(version))

                self.voldemort.put(self._key(pk, field_id, 'value', version),      str(value))
                self.voldemort.put(self._key(pk, field_id, 'source', version),     str(source))
                self.voldemort.put(self._key(pk, field_id, 'timestamp', version),  str(timestamp))
        ### hack code
        # get fields is not exists
        for f in data.iterkeys():
            if f not in self.fields.iterkeys():
                field_not_exist.append(f)
        return field_not_exist

    def history(self, pk, field_id):
        if self.model.objects.filter(code=pk).count() == 0:
            return None

        max_version = 0
        record = self.voldemort.get(self._key(pk, field_id, 'max_version'))
        if len(record) == 0:
            return []
        max_version = int(record[0][0])

        data = {}
        keys = []
        for i in range(1, max_version+1):
            keys.append(self._key(pk, field_id, 'value', i))
            keys.append(self._key(pk, field_id, 'source', i))
            keys.append(self._key(pk, field_id, 'timestamp', i))
            data[i] = {
                'version':   i,
                'value':     None,
                'source':    None,
                'timestamp': None,
            }
        records = self.voldemort.get_all(keys)
        for k in records.iterkeys():
            (pk, field_id, tag, version) = self._extract_key(k)
            data[version][tag] = records[k][0][0]
            if tag == 'value':
                data[version][tag] = self._deserialize(field_id, data[version][tag])

        return data.values()
    def delete(self, pk):
        self.model.objects.filter(code=pk).delete()

        for field_id in self.fields.iterkeys():
            record = self.voldemort.get(self._key(pk, field_id, 'max_version'))
            if len(record) > 0:
                max_version = int(record[0][0])

                self.voldemort.delete(self._key(pk, field_id, 'value'))
                self.voldemort.delete(self._key(pk, field_id, 'source'))
                self.voldemort.delete(self._key(pk, field_id, 'timestamp'))
                self.voldemort.delete(self._key(pk, field_id, 'version'))
                self.voldemort.delete(self._key(pk, field_id, 'max_version'))

                for i in range(1, max_version+1):
                    self.voldemort.delete(self._key(pk, field_id, 'value', i))
                    self.voldemort.delete(self._key(pk, field_id, 'source', i))
                    self.voldemort.delete(self._key(pk, field_id, 'timestamp', i))
