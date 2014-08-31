#coding:utf-8
from django.db.models.loading import get_model
from django.db import models


class EAManager(models.Manager):
    pass

    # def update_counts(self, article, count=0):
    #     eq = get_model('inventory', 'Equipment').objects.get(article=article)
    #     ea = self.get(hash=eq.hash)
    #
    #     diff = ea.count_in - count
    #     if diff < 0:
    #         return False
    #
    #     ea.count_in -= count
    #     ea.count_out += count
    #     ea.save()
    #
    #     return True
