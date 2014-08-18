#coding:utf-8
from django.views.generic import FormView
from .forms import CreateClientForm


class CreateClientView(FormView):
    template_name = 'users/create_client_form.html'
    form_class = CreateClientForm
    success_url = '/'
