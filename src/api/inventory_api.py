#coding:utf-8
from tastypie.resources import ModelResource
from inventory.models import EA, EquipmentType, Reserve, ReserveEA
from inventory.helpers import get_cache_props
from user_api import UserResource
from .authentication import PtitsynApiKeyAuthentication, AutoregApiKeyAuthentication

from tastypie import http
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import MultiAuthentication, SessionAuthentication


class EquipmentTypeResource(ModelResource):

    class Meta:
        queryset = EquipmentType.objects.all()
        resource_name = 'equipment_type'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']


class EAResource(ModelResource):

    type = fields.ForeignKey(EquipmentTypeResource, 'type', full=True)

    class Meta:
        queryset = EA.objects.select_related('type')
        resource_name = 'ea'
        fields = ['count_in', 'hash']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = MultiAuthentication(AutoregApiKeyAuthentication(),
                                             SessionAuthentication())

    def dehydrate(self, bundle):
        bundle = super(EAResource, self).dehydrate(bundle)
        bundle.data['property'] = get_cache_props(bundle.obj.hash, format=False)
        return bundle


class ReserveResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Reserve.objects.all()
        resource_name = 'reserve'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        authorization = DjangoAuthorization()
        authentication = PtitsynApiKeyAuthentication()


class ReserveEAResource(ModelResource):

    reserve = fields.ForeignKey(ReserveResource, 'reserve')
    ea = fields.ForeignKey(EAResource, 'ea')

    class Meta:
        queryset = ReserveEA.objects.all()
        resource_name = 'reserve_item'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        authorization = DjangoAuthorization()
        authentication = PtitsynApiKeyAuthentication()

    def alter_deserialized_detail_data(self, request, data):
        # проверка может ли пользователь забронировать
        # этот инвентарь в количестве которое он указал
        if EAResource().get_via_uri(data['ea']).count_in < data['count']:
            raise ImmediateHttpResponse(response=http.HttpBadRequest())
        return data
