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

    sms = forms.BooleanField(label=u'sms', help_text=u'Без проверки по SMS', required=False)

    def __init__(self, *args, **kwargs):
        super(CreateClientForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                if type(field.widget) in [forms.TextInput]:
                    field.widget = forms.TextInput(attrs={
                        'placeholder': field.label,
                        'class': 'form-control'})
        email_field = self.fields.get('email')
        email_field.widget = forms.HiddenInput()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'photo',
                  'passport', 'travel_passport', 'drive_license',
                  'phone', 'partner',)


class SmsConfirmForm(forms.Form):

    code = forms.IntegerField(label=u'Код подтверждения',
                              help_text=u'Введите код, посланный на указанный номер по SMS',
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control'
                              }))


class CardCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CardCreateForm, self).__init__(*args, **kwargs)
        user_field = self.fields.get('user')
        user_field.widget = forms.HiddenInput()

        article_field = self.fields.get('article')
        article_field.widget = forms.TextInput(attrs={
            'class': 'form-control'})

    class Meta:
        model = Card
