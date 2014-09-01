#coding:utf-8
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm,\
    UserChangeForm as BaseUserChangeForm
from django import forms

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
        self.fields.get('email').widget = forms.HiddenInput()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'photo',
                  'passport', 'travel_passport', 'drive_license',
                  'phone', 'partner',)


class SmsConfirmForm(forms.Form):

    code = forms.IntegerField(label=u'Код подтверждения',
                              help_text=u'Введите код, посланный на указанный '
                                        u'номер по SMS')


class CardCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CardCreateForm, self).__init__(*args, **kwargs)
        self.fields.get('user').widget = forms.HiddenInput()

    class Meta:
        model = Card


class CardCheckForm(forms.Form):

    card = forms.CharField(label=u'Номер карты', max_length=16,
                           widget=forms.TextInput(attrs={
                               'placeholder': u'Номер карты'}))
