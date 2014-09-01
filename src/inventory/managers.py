#coding:utf-8
from django.db.models.loading import get_model
from django.db import models

from .helpers import get_cache_props


class EAManager(models.Manager):

    def free_inventory(self):
        return [{'t': t, 'c': c, 'h': get_cache_props(h)}
                for t, c, h in self.values_list('type__name', 'count_in', 'hash')]
