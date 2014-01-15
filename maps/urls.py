from django.conf.urls import patterns, include, url
from tastypie.api import Api

from .api import MapResource, ThemeResource, MapRequestResource, \
    CountryResource, FormatResource, MapSizeResource, \
    CategoryResource, RequesterResource, SourceResource, UserResource

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
    #url(r'^$', 'views.home', name='home'),
    url(r'', include(api.urls)),

)