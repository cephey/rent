#coding:utf-8
from django.views.generic import FormView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .forms import (CreateClientForm,
                    SmsConfirmForm,
                    CardCreateForm,
                    CardCheckForm)
from .models import User, Sms
from inventory.models import Reserve
from tools.decorators import ajax_required
from .helpers import json_user

import uuid


class CreateClientView(CreateView):
    template_name = 'users/create_client_form.html'
    form_class = CreateClientForm
    next_view = 'users:sms_confirm'

    def get_initial(self):
        self.initial.update({
            'email': '{}@mail.ru'.format(str(uuid.uuid4()).replace('-', '')[:16])
        })
        return self.initial.copy()

    def form_valid(self, form):
        if not form.cleaned_data['phone'] or form.cleaned_data['sms']:
            self.next_view = 'users:add_card'
        return super(CreateClientView, self).form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy(self.next_view,
                                        kwargs={'user': self.object.id})
        return super(CreateClientView, self).get_success_url()


class UpdateClientView(UpdateView):
    template_name = 'users/create_client_form.html'
    form_class = CreateClientForm
    model = User

    def get_success_url(self):
        if not self.object.card_set.all():
            self.success_url = reverse_lazy('users:add_card',
                                            kwargs={'user': self.object.id})
        return super(UpdateClientView, self).get_success_url()


class SmsConfirmView(FormView):
    template_name = 'users/sms_confirm_form.html'
    form_class = SmsConfirmForm
    user_id = None

    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs.get('user')
        return super(SmsConfirmView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        Sms.objects.send_sms_code(self.user_id)
        return super(SmsConfirmView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        User.objects.confirm(self.user_id, form.cleaned_data['code'])
        return super(SmsConfirmView, self).form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy('users:add_card',
                                        kwargs={'user': self.user_id})
        return super(SmsConfirmView, self).get_success_url()


class UserAddCardView(CreateView):
    template_name = 'users/user_add_card_form.html'
    form_class = CardCreateForm
    user_id = None

    def dispatch(self, request, *args, **kwargs):
        self.user_id = kwargs.get('user')
        return super(UserAddCardView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        self.initial.update({'user': self.user_id})
        return self.initial.copy()

    def get_success_url(self):
        self.success_url = reverse_lazy('users:create_success',
                                        kwargs={'user': self.user_id})
        return super(UserAddCardView, self).get_success_url()


class CardCheckView(FormView):
    template_name = 'users/card_check_form.html'
    form_class = CardCheckForm

    @method_decorator(ajax_required)
    def post(self, request, *args, **kwargs):
        return super(CardCheckView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        user = get_object_or_404(User, card__article=form.cleaned_data['card'])
        res, _ = Reserve.objects.get_or_create(user=user, status=Reserve.NEW)

        return JsonResponse({'status': 'success',
                             'user': json_user(user),
                             'reserve': str(res.get_absolute_url())})
