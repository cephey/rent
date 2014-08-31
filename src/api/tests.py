#coding:utf-8
from django.test import TestCase
from tastypie.test import ResourceTestCase
from users.models import User

from inventory.models import Reserve, ReserveEA, EA, EquipmentType


class BaseResourceTestCase(ResourceTestCase):

    def setUp(self):
        super(BaseResourceTestCase, self).setUp()
        self.email = '293013fa8d4c4b48@mail.ru'
        self.user = User.objects.create(email=self.email, is_active=True)

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
