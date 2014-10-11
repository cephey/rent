#coding:utf-8
from users.models import User
from tastypie.validation import Validation


def clear_phone(phone):
    return phone.replace(' ', '').replace('+', '').replace('-', '')\
        .replace('(', '').replace(')', '').replace('\n', '')


class UserValidation(Validation):

    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Нет данных. Пожалуйста добавьте Имя, Фамилию и номер телефона'}

        first_name = bundle.data.get('first_name', None)
        last_name = bundle.data.get('last_name', None)
        phone = bundle.data.get('phone', None)

        if not first_name:
            return {'first_name': 'Не указано Имя'}
        if not last_name:
            return {'last_name': 'Не указана Фамилия'}
        if not phone:
            return {'phone': 'Не указан номер телефона'}
        else:
            if len(clear_phone(phone)) < 7:
                return {'phone': 'Не верно указан номер телефона'}

        # проверка уникальности имени и фамилии
        if request.method.upper() != 'PUT':
            if User.objects.filter(first_name=first_name, last_name=last_name).exists():
                return {'__all__': 'Пользователь с переданными Именем и Фамилией уже существуют'}

        return {}
