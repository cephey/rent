#coding:utf-8
from tastypie.resources import ModelResource, Resource
from inventory.models import EA, EquipmentType, Reserve, ReserveEA
from inventory.helpers import get_cache_props
from user_api import UserResource
from api.paginators import DummyPaginator
from .authentication import PtitsynApiKeyAuthentication

from tastypie import http
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse


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
        # Этот пагинатор позволит избавиться от одного COUNT(*) запроса
        # paginator_class = DummyPaginator

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
        authentication = PtitsynApiKeyAuthentication()
        authorization = DjangoAuthorization()


class ReserveEAResource(ModelResource):

    reserve = fields.ForeignKey(ReserveResource, 'reserve')
    ea = fields.ForeignKey(EAResource, 'ea')

    class Meta:
        queryset = ReserveEA.objects.all()
        resource_name = 'reserve_item'
        # fields = ['count_in', 'hash']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        authentication = PtitsynApiKeyAuthentication()
        authorization = DjangoAuthorization()

    def alter_deserialized_detail_data(self, request, data):
        # проверка может ли пользователь забронировать
        # этот инвентарь в количестве которое он указал
        if EAResource().get_via_uri(data['ea']).count_in < data['count']:
            raise ImmediateHttpResponse(response=http.HttpBadRequest())
        return data
