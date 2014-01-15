import StringIO
from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from maps.models import Map, Theme, MapRequest, Country, Format, \
        MapSize, Category, Requester, Source

sampleimg = StringIO.StringIO('GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
                                                                '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
samplefile = SimpleUploadedFile('test_map.gif', sampleimg.read(), 'image/gif')

def load_test_data(*args):
    load_users()

    if not args:
        raise ValueError('Data type to load not provided')

    if 'themes' in args:
        load_themes()

    if 'categories' in args:
        load_categories()

    if 'countries' in args:
        load_countries()

    if 'formats' in args:
        load_formats()

    if 'sources' in args:
        load_sources()

    if 'sizes' in args:   
        load_map_sizes()

    if 'requesters' in args:
        load_requesters()

    if 'maprequests' in args:
        load_map_requests()

    if 'maps' in args:
        load_maps()

def load_users():
    userdata = testdata['users']
    for user in userdata:
        fields = user['fields']
        user = User.objects.create_user(
            fields['username'],
            fields['email'],
            fields['password'],
        )
        user.is_superuser = fields['is_superuser']
        user.is_staff = fields['is_staff']
        user.last_login = timezone.now()
        user.date_joined = timezone.now()
        user.save()

def load_maps():
    #load neede data
    load_categories()
    load_countries()
    load_sources()
    load_themes()
    load_map_requests()

    mapdata = testdata['maps']

    for themap in mapdata:
        fields = themap['fields']
        Map.objects.create(
            title = fields['title'],
            category = Category.objects.get(slug=fields['category']),
            scale = fields['scale'],
            description = fields['description'],
            country = Country.objects.get(fips=fields['country']),
            center = GEOSGeometry("POINT (0 0)"),
            request = MapRequest.objects.get(title=fields['request']),
            source = Source.objects.get(slug=fields['source']),
            theme = Theme.objects.get(slug=fields['theme']),
            map_thumbnail = samplefile,
            date = datetime.strptime(fields['date'], '%Y-%m-%d'),
            size = MapSize.objects.get(name=fields['size']),
            map_file = samplefile,
        )

def load_themes():
    themedata = testdata['themes']
    for theme in themedata:
        fields = theme['fields']
        Theme.objects.create(
            name = fields['name'],
            slug = fields['slug']
        )

def load_categories():
    catdata = testdata['categories']
    for cat in catdata:
        fields = cat['fields']
        Category.objects.create(
            name = fields['name'],
            slug = fields['slug']
        )

def load_countries():
    coundata = testdata['countries']

    countrysets = []

    for country in coundata:
        fields = country['fields']
        
        #store the country if is composed by other countries
        #to be used at the end to add relationships
        if len(fields['countries']) > 0:
            countrysets.append(country)

        Country.objects.create(
            name = fields['name'],
            iso3 = fields['iso3'],
            iso2 = fields['iso2'],
            fips = fields['fips']
        )

    #add relationships
    for superset in countrysets:
        country = Country.objects.get(fips=superset['fields']['fips'])
        for pk in superset['fields']['countries']:
            country.countries.add(Country.objects.get(fips=superset['fields']['fips']))

def load_formats():
    fordata = testdata['formats']
    for format in fordata:
        fields = format['fields']
        Format.objects.create(
            name = fields['name'],
            resolution = fields['resolution']
        )

def load_requesters():
    reqdata = testdata['requesters']
    for requester in reqdata:
        fields = requester['fields']
        Requester.objects.create(
            name = fields['name'],
            slug = fields['slug']
        )

def load_sources():
    sourcedata = testdata['sources']
    for source in sourcedata:
        fields = source['fields']
        Source.objects.create(
            name = fields['name'],
            slug = fields['slug']
        )

def load_map_sizes():
    sizedata = testdata['mapsizes']
    for size in sizedata:
        fields = size['fields']
        MapSize.objects.create(
            name = fields['name'],
            dimensions = fields['dimensions']
        )

def load_map_requests():
    #load neede data
    load_formats()
    load_map_sizes()
    load_requesters()

    reqdata = testdata['maprequests']
    for req in reqdata:
        fields = req['fields']
        MapRequest.objects.create(
            extended_description = fields['extended_description'],
            title = fields['title'],
            format = Format.objects.filter(name=fields['format'])[0],
            content = fields['content'],
            user = User.objects.get(username=fields['user']),
            requester = Requester.objects.get(slug=fields['requester']),
            date = datetime.strptime(fields['date'], '%Y-%m-%d'),
            size = MapSize.objects.get(name=fields['size']),
            email = fields['email'],
            purpose = fields['purpose']
        )

testdata = {
    "maps": [{
        "fields": {
            "title": "A map",
            "category": "location",
            "scale": "1:500000",
            "description": "A map",
            "country": "ITA",
            "request": "request1",
            "source": "jrc",
            "theme": "crisis",
            "map_thumbnail": "uploads/thumbnails/test.txt",
            "date": "2014-01-08",
            "size": "A4",
            "map_file": "uploads/maps/test.txt"
        }
    },{
        "fields": {
            "title": "Second map",
            "category": "crisis",
            "scale": "1:100000",
            "description": "A map",
            "country": "NOR",
            "request": "request2",
            "source": "jrc",
            "theme": "emergency",
            "map_thumbnail": "uploads/thumbnails/test.txt",
            "date": "2014-01-10",
            "size": "A3",
        }
    }],
    "themes": [{
        "fields": {
            "name": "Crisis",
            "slug": "crisis"
        }
    },
    {
        "fields": {
            "name": "Emergency",
            "slug": "emergency"
        }
    }],
    "countries": [{
        "fields": {
            "iso3": "ITA",
            "iso2": "IT",
            "fips": "ITA",
            "name": "Italy",
            "countries": []
        }
    },
    {
        "fields": {
            "iso3": "NOR",
            "iso2": "NO",
            "fips": "NOR",
            "name": "Norway",
            "countries": []
        }
    },
    {
        "fields": {
            "iso3": "",
            "iso2": "",
            "fips": "WORLD",
            "name": "World",
            "countries": [
                "ITA",
                "NOR"
            ]
        }
    }],
    "formats": [{
        "fields": {
            "resolution": "high",
            "name": "jpg"
        }
    },
    {
        "fields": {
            "resolution": "low",
            "name": "pdf"
        }
    }],
    "mapsizes": [{
        "fields": {
            "name": "A4",
            "dimensions": "12*14"
        }
    },
    {
        "fields": {
            "name": "A3",
            "dimensions": "24*26"
        }
    }],
    "categories": [{
        "fields": {
            "name": "Location",
            "slug": "location"
        }
    },
    {
        "fields": {
            "name": "Crisis",
            "slug": "crisis"
        }
    }],
    "requesters": [{
        "fields": {
            "name": "Johnny",
            "slug": "johnny"
        }
    },
    {
        "fields": {
            "name": "Francis",
            "slug": "francis"
        }
    }],
    "sources": [{
        "fields": {
            "name": "JRC",
            "slug": "jrc"
        }
    },
    {
        "fields": {
            "name": "WFP",
            "slug": "wfp"
        }
    }],
    "users": [{
        "fields": {
            "username": "simone",
            "first_name": "",
            "last_name": "",
            "is_active": True,
            "is_superuser": True,
            "is_staff": True,
            "last_login": "2014-01-07T13:53:42.376Z",
            "groups": [],
            "user_permissions": [],
            "password": "thepwd",
            "email": "",
            "date_joined": "2014-01-07T13:51:54.769Z"
        }
    }],
    "maprequests": [{
        "fields": {
            "extended_description": "I need a map",
            "title": "request1",
            "format": "jpg",
            "content": "With something in it",
            "user": "simone",
            "requester": "francis",
            "date": "2014-01-08",
            "size": "A4",
            "email": "s@d.com",
            "purpose": "To help out"
        }
    },{
        "fields": {
            "extended_description": "A map of Norway",
            "title": "request2",
            "format": "pdf",
            "content": "With something in it",
            "user": "simone",
            "requester": "johnny",
            "date": "2014-01-10",
            "size": "A3",
            "email": "s@d.com",
            "purpose": "To help out"
        }
    }]
}
