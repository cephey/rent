#coding:utf-8
from tastypie.authentication import ApiKeyAuthentication
from tastypie.http import HttpUnauthorized


class PtitsynApiKeyAuthentication(ApiKeyAuthentication):

    def is_authenticated(self, request, **kwargs):
        """
        Переопределяю так как падает авторизация из-за того что для django 1.7
        в tastypie сделали User и username_field ленивыми
        """
        from users.models import User

        try:
            email, api_key = self.extract_credentials(request)
        except ValueError:
            return self._unauthorized()

        if not email or not api_key:
            return self._unauthorized()

        try:
            lookup_kwargs = {'email': email}
            user = User.objects.get(**lookup_kwargs)
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return self._unauthorized()

        if not self.check_active(user):
            return False

        key_auth_check = self.get_key(user, api_key)
        if key_auth_check and not isinstance(key_auth_check, HttpUnauthorized):
            request.user = user

        return key_auth_check


class AutoregApiKeyAuthentication(ApiKeyAuthentication):

    def is_authenticated(self, request, **kwargs):
        """
        Плюшевая аутентификация для авторегов
        """
        try:
            email, api_key = self.extract_credentials(request)
        except ValueError:
            return self._unauthorized()

        if not email or not api_key:
            return self._unauthorized()

        if email != 'autoreg@rent.ru' or api_key != 'a78b786576544c36b2fa6ad339bd460a':
            return self._unauthorized()

        return True
