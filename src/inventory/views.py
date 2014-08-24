#coding:utf-8
from django.views.generic import FormView, CreateView, UpdateView
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404
from django.core import serializers

from .forms import ReserveForm, EAForm
from users.models import User
from tools.views import JSONView
from .models import EA


class ReserveCreateView(FormView):
    template_name = 'inventory/create_reserve_form.html'
    form_class = ReserveForm
    user = None

    def get(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, pk=kwargs.get('user'))
        return super(ReserveCreateView, self).get(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update({'user': self.user})
        return self.initial.copy()


class ReserveUpdateView(UpdateView):
    template_name = 'inventory/update_reserve_form.html'
    form_class = ReserveForm


class EAView(JSONView):

    def get_context_data(self, **kwargs):
        table = serializers.serialize("json", EA.objects.all(),
                                      fields=('type', 'count_in', 'hash'))
        kwargs['ea_table'] = table
        return kwargs
