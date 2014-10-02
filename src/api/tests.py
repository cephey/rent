#coding:utf-8
from django.test import TestCase
from tastypie.test import ResourceTestCase
from users.models import User, Card

from inventory.models import Reserve, ReserveEA, EA, EquipmentType


class BaseResourceTestCase(ResourceTestCase):

    def setUp(self):
        super(BaseResourceTestCase, self).setUp()
        self.email = '293013fa8d4c4b48@mail.ru'
        self.user = User.objects.create(email=self.email)

    def get_credentials(self):
        return self.create_apikey(self.email, self.user.api_key.key)


class ReserveResourceTest(BaseResourceTestCase):

    def test_create(self):
        self.assertEqual(Reserve.objects.count(), 0)

        post_data = {'user': '/api/v1/users/{}/'.format(self.user.id)}
        resp = self.api_client.post('/api/v1/reserve/', data=post_data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertEqual(Reserve.objects.count(), 1)
        self.assertEqual(Reserve.objects.first().user.email, self.email)


class ReserveEAResourceTest(BaseResourceTestCase):

    def setUp(self):
        super(ReserveEAResourceTest, self).setUp()
        # create EA
        eq_type = EquipmentType.objects.create(name='test_equipment_type')
        self.ea = EA.objects.create(type=eq_type, count_in=2, count_out=5, hash='test_hash')

        # create Reserve
        post_data = {'user': '/api/v1/users/{}/'.format(self.user.id)}
        self.api_client.post('/api/v1/reserve/', data=post_data,
                             authentication=self.get_credentials())

    def test_create(self):
        self.assertEqual(ReserveEA.objects.count(), 0)

        self.reserve = Reserve.objects.get(user=self.user)
        post_data = {
            'reserve': '/api/v1/reserve/{}/'.format(self.reserve.id),
            'ea': '/api/v1/ea/{}/'.format(self.ea.id),
            'count': 1
        }

        resp = self.api_client.post('/api/v1/reserve_item/', data=post_data,
                                    authentication=self.get_credentials())
        self.assertHttpCreated(resp)
        self.assertEqual(ReserveEA.objects.count(), 1)


class UserResourceTest(BaseResourceTestCase):

    def test_get_list(self):
        self.email2 = 'rerge7gr5gerg@mail.ru'
        self.user2 = User.objects.create(email=self.email2)

        resp = self.api_client.get('/api/v1/users/', authentication=self.get_credentials())
        objects = self.deserialize(resp)['objects']
        meta = self.deserialize(resp)['meta']

        self.assertEqual(len(objects), 2)
        self.assertEqual(meta['total_count'], 2)

        self.assertEqual(objects[0]['email'], self.email2)
        self.assertEqual(objects[1]['email'], self.email)

    def test_get_detail(self):
        resp = self.api_client.get('/api/v1/users/{}/'.format(1),
                                   authentication=self.get_credentials())
        user = self.deserialize(resp)
        self.assertEqual(user['email'], self.email)
        self.assertFalse(user['confirm'])
        self.assertTrue(user['is_active'])
        self.assertEqual(user['api_key']['key'], self.user.api_key.key)

    def test_card_binding(self):
        self.art = '1324354657687980'
        Card.objects.create(user=self.user, article=self.art)

        self.email2 = 'rerge7gr5gerg@mail.ru'
        self.user2 = User.objects.create(email=self.email2)
        self.art2 = '9870532321412331'

        Card.objects.create(user=self.user2, article=self.art2)

        resp = self.api_client.get('/api/v1/users/',
                                   data={'cards__article': self.art},
                                   authentication=self.get_credentials())
        objects = self.deserialize(resp)['objects']
        meta = self.deserialize(resp)['meta']

        self.assertEqual(len(objects), 1)
        self.assertEqual(meta['total_count'], 1)

        self.assertEqual(objects[0]['email'], self.email)
        self.assertEqual(len(objects[0]['cards']), 1)
        self.assertEqual(objects[0]['cards'][0]['article'], self.art)
        self.assertEqual(objects[0]['api_key']['key'], self.user.api_key.key)


class CardResourceTest(BaseResourceTestCase):

    def setUp(self):
        super(CardResourceTest, self).setUp()
        self.art = '1324354657687980'
        Card.objects.create(user=self.user, article=self.art)

    def test_get_list(self):
        self.email2 = 'rerge7gr5gerg@mail.ru'
        self.user2 = User.objects.create(email=self.email2)
        self.art2 = '9870532321412331'
        Card.objects.create(user=self.user2, article=self.art2)

        resp = self.api_client.get('/api/v1/cards/', authentication=self.get_credentials())
        objects = self.deserialize(resp)['objects']
        meta = self.deserialize(resp)['meta']

        self.assertEqual(len(objects), 2)
        self.assertEqual(meta['total_count'], 2)

        self.assertEqual(objects[0]['article'], self.art)
        self.assertEqual(objects[0]['user']['email'], self.email)

        self.assertEqual(objects[1]['article'], self.art2)
        self.assertEqual(objects[1]['user']['email'], self.email2)

    def test_get_detail(self):
        resp = self.api_client.get('/api/v1/cards/{}/'.format(1),
                                   authentication=self.get_credentials())
        card = self.deserialize(resp)
        self.assertEqual(card['article'], self.art)
        self.assertEqual(card['user']['email'], self.email)
        self.assertEqual(card['user']['api_key']['key'], self.user.api_key.key)
