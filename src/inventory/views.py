#coding:utf-8
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (CreateView,
                                  DeleteView,
                                  DetailView,
                                  RedirectView)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import EA, Reserve, Equipment, ReserveEquipment
from .forms import ReserveEquipmentForm
from .helpers import add_inventory
from tools.views import JSONView


class ReserveEquipmentCreateView(CreateView):
    template_name = 'inventory/create_reserve_form.html'
    form_class = ReserveEquipmentForm

    def dispatch(self, request, *args, **kwargs):
        self.reserve = get_object_or_404(Reserve, id=kwargs.get('pk'))
        return super(ReserveEquipmentCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update({'reserve': self.reserve.id})
        return self.initial.copy()

    def form_valid(self, form):
        article = form.cleaned_data['article']
        success = add_inventory(self.reserve, article)

        if not success:
            return JsonResponse({'errors': {
                '__all__': [_('This inventory is not available')]}})

        self.object = form.save(commit=False)
        self.object.equipment = Equipment.objects.get(article=article)
        self.object.save()

        return JsonResponse(dict(status='success', **self.response))

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors})

    def get_context_data(self, **kwargs):
        context = super(ReserveEquipmentCreateView, self).get_context_data(**kwargs)
        context.update(dict(reserve_id=self.reserve.id, **self.response))
        return context

    @property
    def response(self):
        return {'ea_table': self.reserve.items(),
                'adding': self.reserve.adding_equipment()}


class ReserveEquipmentDeleteView(DeleteView):
    model = ReserveEquipment

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        reserve = self.object.reserve
        self.object.delete()
        return JsonResponse({'status': 'success',
                             'ea_table': reserve.items()})


class ReserveView(DetailView):
    template_name = 'inventory/reserve_confirm.html'
    model = Reserve

    def get_context_data(self, **kwargs):
        context = super(ReserveView, self).get_context_data(**kwargs)
        context['ea_table'] = self.object.current_equipments()
        return context


class ReserveSuccessView(RedirectView):
    permanent = False
    url = '/'

    def get(self, request, *args, **kwargs):
        reserve = get_object_or_404(Reserve, id=kwargs.get('pk'))
        reserve.confirm()
        return super(ReserveSuccessView, self).get(request, *args, **kwargs)


class EAView(JSONView):

    def get_context_data(self, **kwargs):
        context = super(EAView, self).get_context_data(**kwargs)
        context['ea_table'] = EA.objects.free_inventory()
        return context
