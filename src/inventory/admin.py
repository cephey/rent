#coding:utf-8
from django.contrib import admin

from .models import EquipmentType, Equipment, PropertyType, Property, EA, Reserve
from .mixins import PropertyMixin
from .helpers import get_cache_props, get_cache_type

import hashlib
from collections import Counter


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    pass


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 1


@admin.register(Equipment)
class EquipmentAdmin(PropertyMixin, admin.ModelAdmin):
    list_display = ('type', 'article', 'count', '_property')
    inlines = [PropertyInline]

    def response_add(self, request, new_object, post_url_continue=None):
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super(EquipmentAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super(EquipmentAdmin, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):
        # вычисляю хеш (тип + основные свойства)
        props = obj.property_set.filter(general=True)
        hash_base = u'_'.join([
            obj.type.name,
            u'_'.join([u'{}_{}'.format(p.type.name, p.value) for p in props])])
        obj.hash = hashlib.md5(hash_base.encode('utf-8')).hexdigest()
        obj.save()

        # нормализуем количество
        live_hash = Equipment.objects.values_list('hash', flat=True).distinct()
        for item_hash in live_hash:
            eq_sum = sum(Equipment.objects.filter(hash=item_hash).values_list('count', flat=True))
            try:
                ea = EA.objects.get(hash=item_hash)
                diff = eq_sum - (ea.count_in + ea.count_out)
                if diff:
                    ea.count_in += diff
                    ea.save()
            except EA.DoesNotExist:
                EA.objects.create(type=obj.type, count_in=obj.count, hash=item_hash)

        # удаляем те, у которых невалидный хеш
        # случай, когда у товара меняется хеш на новый
        # и в он был единственным представителем старого хеша
        EA.objects.exclude(hash__in=live_hash).delete()

        return obj


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    pass


@admin.register(EA)
class EAAdmin(PropertyMixin, admin.ModelAdmin):
    list_display = ('type', 'count_in', 'count_out', '_property')


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', '_inventory', '_reserve')

    def _inventory(self, obj):
        """
        return: (4)Ботинки => Размер: 40 , (1)Сноуборд => Длина: 160, ...
        """
        eqs = [u'{} => {}'.format(get_cache_type(item.hash), get_cache_props(item.hash))
               for item in obj.equipments.all()]
        return u' , '.join([u'({}){}'.format(v, k)
                            for k, v in Counter(eqs).items()])
    _inventory.short_description = u'Инвентарь на руках'

    def _reserve(self, obj):
        """
        return: (4)Ботинки => Размер: 40 , (1)Сноуборд => Длина: 160, ...
        """
        eqs = [u'({}){} => {}'.format(item.count, get_cache_type(item.ea.hash), get_cache_props(item.ea.hash))
               for item in obj.reserveea_set.select_related('ea__hash').order_by('-count')]
        return u' , '.join(eqs)
    _reserve.short_description = u'Забронировано'
