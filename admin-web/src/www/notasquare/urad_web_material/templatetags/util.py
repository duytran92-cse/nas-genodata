from datetime import datetime, timedelta
from django import template
from django.utils.timesince import timesince
import ast, json

register = template.Library()

@register.filter(name='age')
def age(value):
    if value is None:
        return value
    now = datetime.today()
    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    difference = now - value

    try:
        difference = now - value
    except:
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'

    time = '%(time)s' % {'time': timesince(value).split(', ')[0]}
    for i in ['years', 'months', 'weeks', 'days','hours','minutes', 'day','week','month','year','hour','minute']:
        if i in time:
            time = time.replace(i, i[:1])
    return time.decode('unicode_escape').encode('ascii','ignore')

@register.filter(name='show_format')
def show_format(value):
    if value is None:
        return ''
    if type(value) == unicode:
        try:
            value = json.loads(value)
        except Exception as e:
            return value
    if type(value) == int:
        return value
    return json.dumps(value, indent=4)

@register.filter(name='check')
def check(value):
    if value is None:
        return ''
    return value
