#coding:utf-8
from django.core import serializers

import json


def json_user(user):
    """"""
    obj = json.loads(
        serializers.serialize("json", [user], fields=(
            'first_name', 'last_name', 'patronymic', 'passport',
            'travel_passport', 'drive_license')))

    if user.photo:
        obj[0]['fields']['photo_url'] = user.photo.url

    if not user.card_set.all():
        obj[0]['fields']['profile_url'] = user.get_absolute_url()

    return json.dumps(obj)
