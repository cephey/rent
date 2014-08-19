# coding:utf-8
from django import template

register = template.Library()


@register.filter(name='add_attributes')
def add_attributes(field, css):
    """
    Set class and attribute value to field:
        FROM  'active,form-control,value:100'
        TO    class="active form-control" value="100"
    """
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.as_widget(attrs=attrs)