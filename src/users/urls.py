#coding:utf-8
from django.conf.urls import patterns, url
from .views import CreateClientView

urlpatterns = patterns('',

    url(r'^create/$', CreateClientView.as_view(), name='create'),
)
