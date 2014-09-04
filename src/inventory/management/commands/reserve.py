#coding:utf-8
from django.core.management.base import BaseCommand

from inventory.models import EA, Reserve
from tastypie.test import TestApiClient
from users.models import User, Card

import logging
logger = logging.getLogger('ea')


class Command(BaseCommand):
    help = u'Создание тестовой Брони через API'

    def handle(self, *args, **options):
        logger.info(u'Старт')
        api_client = TestApiClient()

        test_email = 'test_user@mail.ru'
        User.objects.filter(email=test_email).delete()
        user = User.objects.create(email=test_email, first_name=u'Тест', patronymic='Тестович')
        api_key = 'ApiKey {}:{}'.format(user.email, user.api_key.key)
        logger.info(u'Создал пользователя')

        Card.objects.create(user=user, article='777')
        logger.info(u'Привязал карту')

        data = {'user': '/api/v1/users/{}/'.format(user.id)}
        api_client.post('/api/v1/reserve/', data=data, authentication=api_key)
        reserve = Reserve.objects.get(user=user)
        logger.info(u'Создал Бронь № {}'.format(reserve.id))

        ea1 = EA.objects.filter(count_in__gte=2).first()
        data = {
            'reserve': '/api/v1/reserve/{}/'.format(reserve.id),
            'ea': '/api/v1/ea/{}/'.format(ea1.id),
            'count': 2
        }
        api_client.post('/api/v1/reserve_item/', data=data, authentication=api_key)

        ea2 = EA.objects.filter(count_in__gte=1).exclude(id=ea1.id).first()
        data = {
            'reserve': '/api/v1/reserve/{}/'.format(reserve.id),
            'ea': '/api/v1/ea/{}/'.format(ea2.id),
            'count': 1
        }
        api_client.post('/api/v1/reserve_item/', data=data, authentication=api_key)
        logger.info(u'Добавил в бронь 3 вещи')

        logger.info(u'Конец')
