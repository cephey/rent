#coding:utf-8
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (CreateView,
                                  DeleteView,
                                  DetailView,
                                  RedirectView,
                                  FormView)
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseRedirect

from .models import EA, Reserve, Equipment, ReserveEquipment
from .forms import (ReserveEquipmentForm,
                    ReserveCheckForm,
                    ContractForm,
                    ContractPriceForm)
from .helpers import add_inventory
from tools.decorators import ajax_required
from tools.views import JSONView
from users.models import User
from users.helpers import json_user


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


class ReserveCheckView(FormView):
    template_name = 'inventory/reserve_check_form.html'
    form_class = ReserveCheckForm

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        return super(ReserveCheckView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        user = get_object_or_404(User,
                                 reserve__id=form.cleaned_data['reserve'],
                                 reserve__status=Reserve.NEW)
        res = Reserve.objects.get(id=form.cleaned_data['reserve'])

        return JsonResponse({'status': 'success',
                             'user': json_user(user),
                             'reserve': str(res.get_absolute_url())})


class ClientReadyView(JSONView):

    def get_context_data(self, **kwargs):
        context = super(ClientReadyView, self).get_context_data(**kwargs)
        context['cl_table'] = User.objects.ready_for_pay()
        return context


class ContractView(CreateView):
    template_name = 'inventory/create_contract_form.html'
    form_class = ContractForm
    success_url = reverse_lazy('inventory:cashbox')

    def dispatch(self, request, *args, **kwargs):
        self.reserve = get_object_or_404(Reserve, id=kwargs.get('pk'))
        return super(ContractView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update({
            'reserve': self.reserve.id,
            'active': True
        })
        return self.initial.copy()

    def get_context_data(self, **kwargs):
        context = super(ContractView, self).get_context_data(**kwargs)
        context['fio'] = self.reserve.user.get_full_name()
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.reserve.status = Reserve.PAID
        self.reserve.save()
        return HttpResponseRedirect(self.get_success_url())


class ContractPriceView(FormView):
    form_class = ContractPriceForm

    def get(self, request, *args, **kwargs):
        raise Http404

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        return super(ContractPriceView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        reserve_id = form.cleaned_data['reserve']
        period_id = form.cleaned_data['period']

        total = 0
        res = ReserveEquipment.objects.filter(reserve_id=reserve_id)
        for r_eq in res:
            price = r_eq.equipment.prices_set.filter(period_id=period_id)
            total += price[0].value if price else 0

        return JsonResponse({'status': 'success',
                             'sum': total})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors})
