from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'atlas.views.home', name='home'),
    #url(r'^maps/', include('maps.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
