#coding:utf-8
from django.db.models.loading import get_model
from django.core.cache import cache

import random


def get_cache_props(hash):
    prop = cache.get(hash)
    if not prop:
        prop = ','.join([u'{}: {}'.format(name, val)
                         for name, val in get_model('inventory', 'Property')
                .objects.filter(equipment__hash=hash)
                .values_list('type__name', 'value')
                .distinct()])
        cache.set(hash, prop, timeout=random.randint(25 * 60, 35 * 60))
    return prop
