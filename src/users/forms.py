#coding:utf-8
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm,\
    UserChangeForm as BaseUserChangeForm
from django import forms
from .models import User



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
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'patronymic', 'photo',
                  'passport', 'travel_passport', 'drive_license',
                  'phone', 'partner')