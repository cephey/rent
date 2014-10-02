#coding:utf-8
from users.models import User, Card

from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.models import ApiKey


class ApiKeyResource(ModelResource):

    class Meta:
        queryset = ApiKey.objects.all()
        allowed_methods = []


class ShortUserResource(ModelResource):

    api_key = fields.OneToOneField('api.user_api.ApiKeyResource', attribute='api_key', full=True)

    class Meta:
        queryset = User.objects.order_by('-date_joined')
        resource_name = 'users'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'cards': ALL_WITH_RELATIONS
        }


class UserResource(ShortUserResource):

    cards = fields.ManyToManyField('api.user_api.ShortCardResource', attribute='cards', full=True)


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
