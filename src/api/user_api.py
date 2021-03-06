#coding:utf-8
from users.models import User, Card
from api.authentication import PtitsynApiKeyAuthentication, AutoregApiKeyAuthentication
from api.validators import UserValidation

from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authentication import MultiAuthentication, SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.models import ApiKey
from tastypie import fields


class ApiKeyResource(ModelResource):

    class Meta:
        queryset = ApiKey.objects.all()
        allowed_methods = []


class ShortUserResource(ModelResource):

    api_key = fields.OneToOneField('api.user_api.ApiKeyResource',
                                   attribute='api_key', full=True,
                                   readonly=True)

    class Meta:
        queryset = User.objects.order_by('-date_joined')
        resource_name = 'users'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put']
        authorization = Authorization()
        authentication = MultiAuthentication(PtitsynApiKeyAuthentication(),
                                             SessionAuthentication())
        always_return_data = True
        validation = UserValidation()


class UserResource(ShortUserResource):

    cards = fields.ManyToManyField('api.user_api.ShortCardResource',
                                   attribute='cards', full=True,
                                   readonly=True)


class RegUserResource(UserResource):

    class Meta(UserResource.Meta):
        resource_name = 'autoreg'
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = None
        filtering = {
            'cards': ALL_WITH_RELATIONS
        }
        authentication = MultiAuthentication(AutoregApiKeyAuthentication(),
                                             SessionAuthentication())


class ShortCardResource(ModelResource):

    class Meta:
        queryset = Card.objects.order_by('article')
        resource_name = 'cards'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'article': ['exact']
        }


class CardResource(ShortCardResource):

    user = fields.ForeignKey('api.user_api.ShortUserResource', attribute='user', full=True)
