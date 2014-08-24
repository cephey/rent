#coding:utf-8
from django.db import models
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

import hashlib


class EquipmentType(models.Model):

    name = models.CharField(u'Название', max_length=255)

    class Meta:
        ordering = ['name']
        verbose_name = _('equipment type')
        verbose_name_plural = _('equipment types')

    def __unicode__(self):
        return unicode(self.name)


class Equipment(models.Model):

    article = models.CharField(u'Код товара', max_length=16)
    type = models.ForeignKey('inventory.EquipmentType', verbose_name=u'Тип')
    count = models.PositiveIntegerField(u'Количество', blank=True, default=0)
    hash = models.CharField(u'Хеш', max_length=64, editable=False)

    class Meta:
        ordering = ['type']
        verbose_name = _('equipment')
        verbose_name_plural = _('equipments')


def ea_normalize(sender, instance, **kwargs):
    try:
        ea = EA.objects.get(hash=instance.hash)
        diff = ea.count_in + ea.count_out - instance.count
        if diff:
            if ea.count_in >= instance.count:
                ea.count_in -= instance.count
            else:
                ea.count_in = 0
                diff = instance.count - ea.count_in
                if diff > ea.count_out:
                    ea.count_out = 0
                else:
                    ea.count_out -= diff
            ea.save()
        else:
            ea.delete()
    except EA.DoesNotExist:
        pass

post_delete.connect(ea_normalize, sender=Equipment)


class PropertyType(models.Model):

    name = models.CharField(u'Название', max_length=255)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('property type')
        verbose_name_plural = _('type of properties')


class Property(models.Model):

    type = models.ForeignKey('inventory.PropertyType', verbose_name=u'Тип')
    value = models.CharField(u'Значение', max_length=255)
    equipment = models.ForeignKey('inventory.Equipment', verbose_name=u'Оборудование')
    general = models.BooleanField(u'Основное', default=False)

    class Meta:
        ordering = ['type']
        verbose_name = _('property')
        verbose_name_plural = _('properties')


class EA(models.Model):

    type = models.ForeignKey('inventory.EquipmentType', verbose_name=u'Тип')
    count_in = models.PositiveIntegerField(u'Количество на складе', blank=True, default=0)
    count_out = models.PositiveIntegerField(u'Количество в аренде', blank=True, default=0)
    hash = models.CharField(u'Хеш', max_length=64, unique=True, editable=False)

    class Meta:
        ordering = ['type']
        verbose_name = _('unit')
        verbose_name_plural = _('units')


class Reserve(models.Model):

    user = models.ForeignKey('users.User', verbose_name=u'Клиент')
    eas = models.ManyToManyField('inventory.EA')

    class Meta:
        verbose_name = _('reserve')
        verbose_name_plural = _('reserve')

    def get_absolute_url(self):
        return reverse_lazy('inventory:reserve', kwargs={'pk': self.pk})
