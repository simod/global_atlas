from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from tastypie.api import Api
from django_downloadview import ObjectDownloadView

from .api import MapResource, ThemeResource, MapRequestResource, \
    CountryResource, FormatResource, MapSizeResource, \
    CategoryResource, RequesterResource, SourceResource, UserResource, \
    CollinsMapResource
from .views import Home
from .models import Map, CollinsMap


api = Api(api_name='api')
api.register(MapResource())
api.register(ThemeResource())
api.register(MapRequestResource())
api.register(FormatResource())
api.register(MapSizeResource())
api.register(CategoryResource())
api.register(RequesterResource())
api.register(SourceResource())
api.register(CountryResource())
api.register(UserResource())
api.register(CollinsMapResource())

map_download = ObjectDownloadView.as_view(model=Map, file_field='map_file')
collins_download = ObjectDownloadView.as_view(model=CollinsMap, file_field='the_file')

urlpatterns = patterns('',
    # Examples:
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^$', login_required(Home.as_view())),
    url(r'^help/?$', TemplateView.as_view(template_name="help.html")),
    url(r'^maps/(?P<pk>[0-9]+)/download/?$', login_required(map_download), name='map_download'),
    url(r'^collins/(?P<pk>[0-9]+)/download/?$', login_required(collins_download), name='collins_download'),
    url(r'', include(api.urls)),
)