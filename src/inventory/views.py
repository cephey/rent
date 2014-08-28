#coding:utf-8
from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .forms import ReserveForm, ReserveEquipmentForm
from tools.views import JSONView
from .models import EA, Reserve, Equipment
from .helpers import get_cache_props

ALREADY_RESERVE = u'Это снаряжение уже кем-то забронировано.'


class ReserveUpdateView(UpdateView):
    template_name = 'inventory/create_reserve_form.html'
    form_class = ReserveForm
    model = Reserve


class ReserveEquipmentCreateView(CreateView):
    template_name = 'inventory/create_reserve_form.html'
    form_class = ReserveEquipmentForm
    reserve = None

    def dispatch(self, request, *args, **kwargs):
        self.reserve = get_object_or_404(Reserve, id=kwargs.get('pk'))
        return super(ReserveEquipmentCreateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update({'reserve': self.reserve.id})
        return self.initial.copy()

    def form_valid(self, form):
        article = form.cleaned_data['article']
        success = EA.objects.update_counts(article, 1)

        if not success:
            return JsonResponse({'errors': {'__all__': [ALREADY_RESERVE]}})

        self.object = form.save(commit=False)
        self.object.equipment = Equipment.objects.get(article=article)
        self.object.save()

        return JsonResponse({'status': 'success',
                             'ea_table': self.reserve.items()})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors})


class ReserveView(UpdateView):
    template_name = 'inventory/update_reserve_form.html'
    form_class = ReserveForm


class EAView(JSONView):

    def get_context_data(self, **kwargs):
        eas = EA.objects.values_list('type__name', 'count_in', 'hash')

        kwargs['ea_table'] = [{'t': t, 'c': c, 'h': get_cache_props(h)}
                              for t, c, h in eas]
        return kwargs
