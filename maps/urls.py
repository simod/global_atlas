from django.conf.urls import patterns, include, url
from tastypie.api import Api

from .api import MapResource

api = Api(api_name='api')
api.register(MapResource())

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'views.home', name='home'),
    url(r'', include(api.urls)),

)