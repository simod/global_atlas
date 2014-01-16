from django.contrib.auth.models import User

from tastypie.resources import ModelResource
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

from .models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source

class UserResource(ModelResource):
    """User api"""

    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get']
        excludes = ['is_staff', 'password', 'is_superuser',
             'is_active',  'date_joined', 'last_login']

class ThemeResource(ModelResource):
    """Theme api"""

    class Meta:
        queryset = Theme.objects.all()
        resource_name = 'themes'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']


class CategoryResource(ModelResource):
    """Category api"""

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'categories'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

class SourceResource(ModelResource):
    """Source api"""

    class Meta:
        queryset = Source.objects.all()
        resource_name = 'sources'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']


class CountryResource(ModelResource):
    """Country api"""

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'countries'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']


class MapSizeResource(ModelResource):
    """MapSize api"""

    class Meta:
        queryset = MapSize.objects.all()
        resource_name = 'sizes'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']


class FormatResource(ModelResource):
    """Format api"""

    class Meta:
        queryset = Format.objects.all()
        resource_name = 'formats'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']


class RequesterResource(ModelResource):
    """Requester api"""

    class Meta:
        queryset = Requester.objects.all()
        resource_name = 'requesters'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']


class MapRequestResource(ModelResource):
    """MapRequest api"""

    size = fields.ForeignKey(MapSizeResource, 'size')
    format = fields.ForeignKey(FormatResource, 'format')
    requester = fields.ForeignKey(RequesterResource, 'requester')
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = MapRequest.objects.all()
        resource_name = 'requests'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']


class MapResource(GeoModelResource):
    """Map api"""

    theme = fields.ForeignKey(ThemeResource, 'theme')
    category = fields.ForeignKey(CategoryResource, 'category')
    source = fields.ForeignKey(SourceResource , 'source')
    country = fields.ForeignKey(CountryResource , 'country')
    size = fields.ForeignKey(MapSizeResource , 'size')
    request = fields.ForeignKey(MapRequestResource , 'request')

    class Meta:
        queryset = Map.objects.all()
        resource_name = 'maps'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']
