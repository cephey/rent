#coding:utf-8
from django import forms
from .models import Reserve, EA, ReserveEquipment, Equipment


class ReserveForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReserveForm, self).__init__(*args, **kwargs)
        self.fields.get('user').widget = forms.HiddenInput()

    class Meta:
        model = Reserve


class EAForm(forms.ModelForm):

    class Meta:
        model = EA


class ReserveEquipmentForm(forms.ModelForm):

    article = forms.CharField(max_length=16,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ReserveEquipmentForm, self).__init__(*args, **kwargs)
        self.fields.get('reserve').widget = forms.HiddenInput()

    class Meta:
        model = ReserveEquipment
        fields = ('reserve',)

    def clean_article(self):
        data = self.cleaned_data['article']
        try:
            Equipment.objects.get(article=data)
        except Equipment.DoesNotExist:
            raise forms.ValidationError(
                u"Снаряжения с артиклом {} не найдено".format(data))
        return data
