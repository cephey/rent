from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'conf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('pages.urls', namespace='pages')),

    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

