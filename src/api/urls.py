#coding:utf-8
from django.conf.urls import patterns, include, url
from django.http import Http404

from inventory_api import (EAResource,
                           EquipmentTypeResource,
                           ReserveResource,
                           ReserveEAResource)
from user_api import UserResource, CardResource, RegUserResource

from tastypie.api import Api

api = Api(api_name='v1')
api.register(EAResource())
api.register(EquipmentTypeResource())
api.register(ReserveResource())
api.register(ReserveEAResource())

api.register(RegUserResource())
api.register(UserResource())
api.register(CardResource())


def http404(request):
    raise Http404

urlpatterns = patterns(
    '',
    url(r'^v1/?$', http404),
    url(r'', include(api.urls))
)