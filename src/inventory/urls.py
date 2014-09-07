#coding:utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (ReserveView,
                    EAView,
                    ReserveEquipmentCreateView,
                    ReserveEquipmentDeleteView,
                    ReserveSuccessView,
                    ReserveCheckView,
                    ClientReadyView,
                    ContractView,
                    ContractPriceView)

urlpatterns = patterns(
    '',
    url(r'^reserve/(?P<pk>[0-9]+)/$', ReserveEquipmentCreateView.as_view(),
        name='reserve'),
    url(r'^reserve/confirm/(?P<pk>[0-9]+)/$', ReserveView.as_view(),
        name='confirm'),

    url(r'^reserve/success/(?P<pk>[0-9]+)/$', ReserveSuccessView.as_view(),
        name='success'),

    url(r'^reserve_equipment_delete/(?P<pk>[0-9]+)/$',
        ReserveEquipmentDeleteView.as_view(),
        name='reserve_equipment_delete'),

    # Таблица что осталось
    url(r'^ea/$', EAView.as_view(), name='ea'),

    url(r'^reserve_check/$', ReserveCheckView.as_view(), name='reserve_check'),

    # страница кассы
    url(r'^cashbox/$', TemplateView.as_view(template_name='inventory/cashbox.html'),
        name='cashbox'),

    # Таблица готовых к оплате клиентов
    url(r'^cr/$', ClientReadyView.as_view(), name='cr'),

    url(r'^contract/(?P<pk>[0-9]+)/$', ContractView.as_view(), name='contract'),

    # Суммарная цена по договору
    url(r'^contract/price/$', ContractPriceView.as_view(), name='contract_price'),
)
