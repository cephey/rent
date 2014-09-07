#coding:utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ReserveEquipment, Equipment, Contract, Reserve, Period


class ReserveEquipmentForm(forms.ModelForm):

    article = forms.CharField(max_length=16)

    class Meta:
        model = ReserveEquipment
        fields = ('reserve',)
        widgets = {
            'reserve': forms.HiddenInput(),
        }

    def clean_article(self):
        data = self.cleaned_data['article']
        try:
            Equipment.objects.get(article=data)
        except Equipment.DoesNotExist:
            raise forms.ValidationError(
                u"Снаряжения с артиклом {} не найдено".format(data))
        return data


class ReserveCheckForm(forms.Form):

    reserve = forms.CharField(label=u'Номер брони', max_length=16,
                              widget=forms.TextInput(attrs={
                                  'placeholder': u'Номер брони'}))


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        widgets = {
            'deposit': forms.RadioSelect(),
            'reserve': forms.HiddenInput(),
            'active': forms.HiddenInput(),
            'total': forms.HiddenInput(),
        }


class ContractPriceForm(forms.Form):

    reserve = forms.IntegerField()
    period = forms.IntegerField()

    def clean_reserve(self):
        id = self.cleaned_data['reserve']
        if not Reserve.objects.filter(id=id, status=Reserve.RESERVE).exists():
            raise forms.ValidationError(_('Reserve does not exist'))
        return id

    def clean_period(self):
        id = self.cleaned_data['period']
        if not Period.objects.filter(id=id).exists():
            raise forms.ValidationError(_('Period does not exist'))
        return id
