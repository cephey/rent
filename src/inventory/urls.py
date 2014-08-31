#coding:utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (ReserveView,
                    EAView,
                    ReserveEquipmentCreateView,
                    ReserveEquipmentDeleteView,
                    ReserveSuccessView)

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='inventory/all.html'), name='all'),

    # url(r'^reserve/create/(?P<user>[0-9]+)/$', ReserveCreateView.as_view(), name='reserve_create'),
    url(r'^reserve/(?P<pk>[0-9]+)/$', ReserveEquipmentCreateView.as_view(), name='reserve'),
    url(r'^reserve/confirm/(?P<pk>[0-9]+)/$', ReserveView.as_view(), name='confirm'),

    url(r'^reserve/success/(?P<pk>[0-9]+)/$', ReserveSuccessView.as_view(), name='success'),

    # url(r'^reserve_equipment_create/$',
    #     ReserveEquipmentCreateView.as_view(),
    #     name='reserve_equipment_create'),
    url(r'^reserve_equipment_delete/(?P<pk>[0-9]+)/$',
        ReserveEquipmentDeleteView.as_view(),
        name='reserve_equipment_delete'),

    # Таблица что осталось
    url(r'^ea/$', EAView.as_view(), name='ea'),

    # url(r'^sms_confirm/(?P<user>[0-9]+)/$', SmsConfirmView.as_view(), name='sms_confirm'),
    # url(r'^add_card/(?P<user>[0-9]+)/$', UserAddCardView.as_view(), name='add_card'),
    #
    # url(r'^create/success/(?P<user>[0-9]+)/$',
    #     TemplateView.as_view(template_name='users/create_client_success.html'),
    #     name='create_success'),
)
