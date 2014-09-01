#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns(
    '',

    url(r'^api/', include('api.urls')),

    url(r'', include('pages.urls', namespace='pages')),

    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^inventory/', include('inventory.urls', namespace='inventory')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
