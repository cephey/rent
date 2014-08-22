#coding:utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from .views import CreateClientView, SmsConfirmView, UserAddCardView

urlpatterns = patterns(
    '',
    url(r'^create/$', CreateClientView.as_view(), name='create'),
    url(r'^sms_confirm/(?P<user>[0-9]+)/$', SmsConfirmView.as_view(), name='sms_confirm'),
    url(r'^add_card/(?P<user>[0-9]+)/$', UserAddCardView.as_view(), name='add_card'),

    url(r'^create/success/(?P<user>[0-9]+)/$',
        TemplateView.as_view(template_name='users/create_client_success.html'),
        name='create_success'),
)
