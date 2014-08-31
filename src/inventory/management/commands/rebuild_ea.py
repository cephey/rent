#coding:utf-8
from django.core.management.base import BaseCommand, CommandError
from inventory.models import EA, Equipment

import logging
logger = logging.getLogger('ea')


class Command(BaseCommand):
    help = u'Пересборка таблицы EA'

    def handle(self, *args, **options):
        logger.info(u'Старт пересборки таблицы EA')

        # нормализуем количество
        live_hash = Equipment.objects.values_list('hash', flat=True).distinct()
        for item_hash in live_hash:
            eq_sum = sum(Equipment.objects.filter(hash=item_hash).values_list('count', flat=True))
            try:
                ea = EA.objects.get(hash=item_hash)
            except EA.DoesNotExist:
                logger.info(u'EA c хешем {} не найден, хотя он существует в таблице Equipment'.format(item_hash))

            rea_sum = sum(item.count for item in ea.reserveea_set.all())
            ea.count_in = eq_sum - rea_sum
            ea.count_out = rea_sum
            ea.save()
            logger.info(u'EA c хешем {} сохранен'.format(item_hash))

        # удаляем те, для которых нет соответствующего Equipment
        EA.objects.exclude(hash__in=live_hash).delete()
        logger.info(u'Пересборки таблицы EA закончилась')
