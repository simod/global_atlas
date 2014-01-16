from django.contrib.auth.models import User

from tastypie.resources import ModelResource
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL

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

        filtering = {
            'username': ALL,
        }

class ThemeResource(ModelResource):
    """Theme api"""

    class Meta:
        queryset = Theme.objects.all()
        resource_name = 'themes'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'slug': ALL,
            'name': ALL
        }


class CategoryResource(ModelResource):
    """Category api"""

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'categories'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'slug': ALL,
            'name': ALL
        }


class SourceResource(ModelResource):
    """Source api"""

    class Meta:
        queryset = Source.objects.all()
        resource_name = 'sources'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'slug': ALL,
            'name': ALL
        }


class CountryResource(ModelResource):
    """Country api"""

    countries = fields.ToManyField('self', 'countries')

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'countries'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'fips': ALL,
        }


class MapSizeResource(ModelResource):
    """MapSize api"""

    class Meta:
        queryset = MapSize.objects.all()
        resource_name = 'sizes'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'name': ALL,
        }


class FormatResource(ModelResource):
    """Format api"""

    class Meta:
        queryset = Format.objects.all()
        resource_name = 'formats'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'resolution': ALL,
            'name': ALL
        }


class RequesterResource(ModelResource):
    """Requester api"""

    class Meta:
        queryset = Requester.objects.all()
        resource_name = 'requesters'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'slug': ALL,
            'name': ALL
        }


class MapRequestResource(ModelResource):
    """MapRequest api"""

    size = fields.ToOneField(MapSizeResource, 'size')
    format = fields.ToOneField(FormatResource, 'format')
    requester = fields.ToOneField(RequesterResource, 'requester')
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = MapRequest.objects.all()
        resource_name = 'requests'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'title': ALL,
            'requester': ALL
        }


class MapResource(GeoModelResource):
    """Map api"""

    theme = fields.ToOneField(ThemeResource, 'theme')
    category = fields.ToOneField(CategoryResource, 'category')
    source = fields.ToOneField(SourceResource , 'source')
    country = fields.ToOneField(CountryResource , 'country')
    size = fields.ToOneField(MapSizeResource , 'size')
    request = fields.ToOneField(MapRequestResource , 'request')

    class Meta:
        queryset = Map.objects.all()
        resource_name = 'maps'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'title': ALL,
        }
