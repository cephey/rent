#coding:utf-8
from django.views.generic import CreateView
from .forms import CreateClientForm


class CreateClientView(CreateView):
    template_name = 'users/create_client_form.html'
    form_class = CreateClientForm
    success_url = '/'