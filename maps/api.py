from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField
from django.db.models import Count

from tastypie.resources import ModelResource
from tastypie.contrib.gis.resources import ModelResource as GeoModelResource
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.validation import FormValidation
from tastypie.cache import SimpleCache

from .models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source, CollinsMap
from .forms import MapRequestForm


class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]

        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def is_valid(self, bundle, request=None):
        data = bundle.data
        # Ensure we get a bound Form, regardless of the state of the bundle.
        if data is None:
            data = {}
        # copy data, so we don't modify the bundle
        data = data.copy()

        # convert URIs to PK integers for all relation fields
        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if field in data:
                data[field] = self.uri_to_pk(data[field])

        # validate and return messages on error
        form = self.form_class(data)
        if form.is_valid():
            return {}
        return form.errors


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
            'name': ALL,
            'id': ALL
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
            'name': ALL,
            'id': ALL
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


class CountryResource(GeoModelResource):
    """Country api"""

    countries = fields.ToManyField('self', 'countries')

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'countries'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']
        cache = SimpleCache(timeout=60000)

        filtering = {
            'fips': ALL,
            'countries': ALL,
            'id': ALL
        }

    def dehydrate(self, bundle):
        bundle.data['type'] = 'Feature'
        bundle.data['maps_count'] = {
            'total': bundle.obj.map_set.count(),
            'counts': list(bundle.obj.map_set. \
            values('category__name').annotate(count=Count('category__name')))
        }  
        
        return bundle

    def get_object_list(self, request):
        """Expose the model manager querysets and apply filters"""
        if request.GET.has_key('type'):
            if request.GET['type'] == 'regions':
                queryset = Country.objects.get_regions()
            else:
                queryset = Country.objects.get_countries()
        else:
            queryset = super(CountryResource, self).get_object_list(request)

        if request.GET.has_key('q'):
            queryset = queryset.filter(name__icontains=request.GET['q'])

        return queryset

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
        
        validation = ModelFormValidation(form_class=MapRequestForm)

    # Set the user as the logged in user
    def obj_create(self, bundle, **kwargs):
        return super(MapRequestResource, self).obj_create(
            bundle, user=bundle.request.user)

class MapResource(GeoModelResource):
    """Map api"""

    theme = fields.ToOneField(ThemeResource, 'theme', full=True)
    category = fields.ToOneField(CategoryResource, 'category', full=True)
    source = fields.ToOneField(SourceResource , 'source', full=True)
    country = fields.ToOneField(CountryResource , 'country')
    size = fields.ToOneField(MapSizeResource , 'size', full=True)
    request = fields.ToOneField(MapRequestResource , 'request')

    def dehydrate(self, bundle):
        bundle.data['country'] = bundle.obj.country.name
        bundle.data['format'] = bundle.obj.request.format.name
        bundle.data['file_size'] = float(bundle.obj.map_file.size) / (1024 * 1024)
        return bundle

    class Meta:
        queryset = Map.objects.all().order_by('-date')
        resource_name = 'maps'
        authentication= SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'title': ALL,
            'country': ALL_WITH_RELATIONS,
            'category': ALL_WITH_RELATIONS,
            'theme': ALL_WITH_RELATIONS,
            'id': ALL
        }

class CollinsMapResource(ModelResource):
    """CollinsMap api"""

    country = fields.ToOneField(CountryResource , 'country')
    
    class Meta:
        queryset = CollinsMap.objects.all()
        resource_name ='collins_maps'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get','post','delete','put']

        filtering = {
            'country': ALL_WITH_RELATIONS,
            'id': ALL
        }