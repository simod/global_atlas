from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization

from .models import Map

class MapResource(ModelResource):
    """Map api"""

    class Meta:
        queryset = Map.objects.all()
        resource_name = 'maps'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']