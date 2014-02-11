from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from tastypie.api import Api
from django_downloadview import ObjectDownloadView

from .api import MapResource, ThemeResource, MapRequestResource, \
    CountryResource, FormatResource, MapSizeResource, \
    CategoryResource, RequesterResource, SourceResource, UserResource
from .views import Home
from .models import Map


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

download = ObjectDownloadView.as_view(model=Map, file_field='map_file')

urlpatterns = patterns('',
    # Examples:
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^$', login_required(Home.as_view())),
    url(r'^maps/(?P<pk>[0-9]+)/download/?$', login_required(download), name='map_download'),
    url(r'', include(api.urls)),
)