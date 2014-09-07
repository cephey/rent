#coding:utf-8
from django.contrib.auth.forms import (UserCreationForm as BaseUserCreationForm,
                                       UserChangeForm as BaseUserChangeForm)
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django import forms

from .widgets import AdminImageWidget
from .models import User, Card


class UserCreationForm(BaseUserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(BaseUserChangeForm):

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['photo'].widget = AdminImageWidget()
        del self.fields['username']

    class Meta:
        model = User


class CreateClientForm(forms.ModelForm):

    sms = forms.BooleanField(label=u'sms', help_text=u'Без проверки по SMS',
                             required=False)

    def __init__(self, *args, **kwargs):
        super(CreateClientForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in [forms.TextInput]:
                    field.widget = forms.TextInput(attrs={
                        'placeholder': field.label,
                        'class': 'form-control'})

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'photo',
                  'passport', 'travel_passport', 'drive_license',
                  'phone', 'partner',)
        widgets = {
            'email': forms.HiddenInput(),
        }


class SmsConfirmForm(forms.Form):

    code = forms.IntegerField(label=u'Код подтверждения',
                              help_text=u'Введите код, посланный на указанный '
                                        u'номер по SMS')


class CardCreateForm(forms.ModelForm):

    class Meta:
        model = Card
        widgets = {
            'user': forms.HiddenInput(),
        }


class CardCheckForm(forms.Form):

    card = forms.CharField(label=u'Номер карты', max_length=16,
                           widget=forms.TextInput(attrs={
                               'placeholder': u'Номер карты'}))


class AuthenticationForm(forms.Form):

    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(
                                 attrs={'placeholder': u'E-mail'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': u'Пароль'}))

    error_messages = {
        'invalid_login': _("Please enter a correct %(email)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'email': self.email_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'],
                                        code='inactive')

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
