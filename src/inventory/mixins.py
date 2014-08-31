#coding:utf-8
from .helpers import get_cache_props


class PropertyMixin(object):

    def _property(self, obj):
        return get_cache_props(obj.hash)
    _property.short_description = u'Основные свойства'
