#coding:utf-8
from django import forms
from .models import Reserve, EA


class ReserveForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReserveForm, self).__init__(*args, **kwargs)
        user_field = self.fields.get('user')
        user_field.widget = forms.HiddenInput()

    class Meta:
        model = Reserve


class EAForm(forms.ModelForm):

    class Meta:
        model = EA
