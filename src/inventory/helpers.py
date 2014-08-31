#coding:utf-8
from django.db.models.loading import get_model
from django.core.cache import cache
from django.db import transaction

import random
from collections import Counter


def get_cache_props(hash, format=True):
    prop = cache.get(hash)
    if not prop:
        prop = list(get_model('inventory', 'Property')
                    .objects.filter(equipment__hash=hash)
                    .values_list('type__name', 'value')
                    .distinct())

        cache.set(hash, prop, timeout=random.randint(25 * 60, 35 * 60))

    if format:
        return ','.join([u'{}: {}'.format(name, val) for name, val in prop])
    return {name: val for name, val in prop}


def get_cache_type(hash):
    hash_name = '{}_type'.format(hash)
    type_name = cache.get(hash_name)
    if not type_name:
        eq = get_model('inventory', 'Equipment')\
            .objects.filter(hash=hash).first()
        type_name = eq.type.name

        cache.set(hash_name, type_name, timeout=random.randint(25 * 60, 35 * 60))
    return type_name


@transaction.atomic
def add_inventory(reserve, article):
    # создать словарь заброненых товаров
    r_ea = {item.ea.hash: item.count
            for item in reserve.reserveea_set.select_related('ea')}
    r_ea = Counter(**r_ea)

    # создать словарь товаров пробитых менеджером
    r_eq = [item.equipment.hash
            for item in reserve.reserveequipment_set.select_related('equipment')]
    r_eq = Counter(r_eq)

    # вычесть из первого второй
    result = r_ea - r_eq

    # TODO: постараться оптимизировать
    eq = get_model('inventory', 'Equipment').objects.get(article=article)

    # если пользователь бранировал товар,
    # то разрешаю привязать его к резерву
    if eq.hash in result:
        if result.get(eq.hash) > 0:
            return True

    ea = get_model('inventory', 'EA').objects.get(hash=eq.hash)

    # если можно забронировать,
    # разрешаю привязать к резерву
    if ea.count_in > 0:
        ReserveEA = get_model('inventory', 'ReserveEA')
        # если товары такого типа есть в брони
        if eq.hash in r_ea:
            # то инкременчу количество
            r_ea = ReserveEA.objects.get(ea__hash=eq.hash)
            r_ea.count += 1
            r_ea.save()
        else:
            # иначе создаю новую связку с бронью
            ReserveEA.objects.create(reserve=reserve, ea=ea, count=1)
        return True

    return False
