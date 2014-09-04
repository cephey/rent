#coding:utf-8
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import LoginView, LogoutView

urlpatterns = patterns(
    '',

    url(r'^$', TemplateView.as_view(template_name='pages/index.html'),
        name='index'),
    url(r'^charts/$', TemplateView.as_view(template_name='pages/charts.html'),
        name='charts'),
    url(r'^tables/$', TemplateView.as_view(template_name='pages/tables.html'),
        name='tables'),
    url(r'^forms/$', TemplateView.as_view(template_name='pages/forms.html'),
        name='forms'),
    url(r'^elements/$', TemplateView.as_view(template_name='pages/elements.html'),
        name='elements'),
    url(r'^grid/$', TemplateView.as_view(template_name='pages/grid.html'),
        name='grid'),
    url(r'^blank/$', TemplateView.as_view(template_name='pages/blank.html'),
        name='blank'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)
