#coding:utf-8
from django.db.models.signals import post_delete, post_save
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db import transaction
from django.db import models

from .managers import EAManager
from helpers import get_cache_props, get_cache_type

from collections import Counter


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


@receiver(post_delete, sender=Equipment)
@transaction.atomic
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

    objects = EAManager()

    class Meta:
        ordering = ['type']
        verbose_name = _('unit')
        verbose_name_plural = _('units')


class Reserve(models.Model):

    NEW = 'NEW'
    RESERVE = 'RES'
    PAID = 'PAID'
    STATUSES = (
        (NEW, u'Новый'),
        (RESERVE, u'Готов к оплате'),
        (PAID, u'Оплачено'),
    )

    user = models.ForeignKey('users.User', verbose_name=u'Клиент')
    equipments = models.ManyToManyField('inventory.Equipment',
                                        through='inventory.ReserveEquipment')
    eas = models.ManyToManyField('inventory.EA',
                                 through='inventory.ReserveEA')
    status = models.CharField(max_length=4, choices=STATUSES, default=NEW)

    def __unicode__(self):
        return u'Reserve: User={}, status={}'.format(self.user, dict(self.STATUSES).get(self.status))

    class Meta:
        verbose_name = _('reserve')
        verbose_name_plural = _('reserve')

    def get_absolute_url(self):
        return reverse('inventory:reserve', kwargs={'pk': self.pk})

    def items(self):
        # TODO: оптимизировать sql
        inventory = self.reserveea_set.all()
        return [{'t': get_cache_type(item.ea.hash),
                 'h': get_cache_props(item.ea.hash),
                 'c': item.count} for item in inventory]

    def current_equipments(self):
        # TODO: оптимизировать sql
        inventory = Counter([item.equipment.hash
                       for item in self.reserveequipment_set.all()])
        return [{'t': get_cache_type(eq_hash),
                 'h': get_cache_props(eq_hash),
                 'c': count} for eq_hash, count in inventory.items()]

    def adding_equipment(self):
        # TODO: оптимизировать sql
        inventory = self.reserveequipment_set.all()
        return [{'t': get_cache_type(item.equipment.hash),
                 'h': get_cache_props(item.equipment.hash),
                 'url': reverse('inventory:reserve_equipment_delete', kwargs={'pk': item.id}),
                 'a': item.equipment.article} for item in inventory]

    @transaction.atomic
    def confirm(self):
        # создать словарь заброненых товаров
        r_ea = {item.ea.hash: item.count
                for item in self.reserveea_set.select_related('ea')}
        r_ea = Counter(**r_ea)

        # создать словарь товаров пробитых менеджером
        r_eq = [item.equipment.hash
                for item in self.reserveequipment_set.select_related('equipment')]
        r_eq = Counter(r_eq)

        # вычесть из первого второй
        result = r_ea - r_eq

        # удаляю/обновляю связки ReserveEA у reserve
        for ea_hash, count in result.items():
            r_ea = ReserveEA.objects.get(reserve=self, ea__hash=ea_hash)
            diff = r_ea.count - count
            if diff:
                r_ea.count = diff
                r_ea.save()
            else:
                r_ea.delete()

        self.status = self.RESERVE
        self.save()


class ReserveEquipment(models.Model):
    """
    Для хранения забронированного инвенторя который пробивает менеджер
    """
    reserve = models.ForeignKey('inventory.Reserve')
    equipment = models.ForeignKey('inventory.Equipment')


class ReserveEA(models.Model):
    """
    Для хранения забронированного инвентаря с api
    """
    reserve = models.ForeignKey('inventory.Reserve')
    ea = models.ForeignKey('inventory.EA')
    count = models.PositiveIntegerField()


@receiver(post_save, sender=ReserveEA)
@receiver(post_delete, sender=ReserveEA)
@transaction.atomic
def update_ea_count(sender, instance, **kwargs):
    ea = instance.ea
    eq_sum = sum(Equipment.objects.filter(hash=ea.hash).values_list('count', flat=True))
    ea.count_out = sum([item.count for item in instance.ea.reserveea_set.all()])
    ea.count_in = eq_sum - ea.count_out
    ea.save()
