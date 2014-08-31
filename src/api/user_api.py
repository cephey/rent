#coding:utf-8
from tastypie.resources import ModelResource, Resource
from users.models import User
from inventory.helpers import get_cache_props

# from tastypie import fields


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
