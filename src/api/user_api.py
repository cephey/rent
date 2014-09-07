#coding:utf-8
from users.models import User

from tastypie.resources import ModelResource


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
