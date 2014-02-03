from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from tastypie.api import Api

from .api import MapResource, ThemeResource, MapRequestResource, \
    CountryResource, FormatResource, MapSizeResource, \
    CategoryResource, RequesterResource, SourceResource, UserResource
from .views import Home


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


urlpatterns = patterns('',
    # Examples:
    #url(r'^$', login_required(Home.as_view())),
    url(r'^$', Home.as_view()),
    url(r'', include(api.urls)),
)