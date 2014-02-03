import json

from django.core.management.base import BaseCommand, CommandError

from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon, fromstr

from maps.models import Country

def import_countries():
    with open('static/app/data/countries.json') as countries:
        the_json = json.loads(countries.read())
        for feature in the_json['features']:
            country, _ = Country.objects.get_or_create(iso3=feature['id'])
            country.name = feature['properties']['name']
            country.fips = feature['id']
            country.iso3 = feature['id']
            the_geom = GEOSGeometry(json.dumps(feature['geometry']))
            if (isinstance(the_geom, Polygon)):
                country.geometry = MultiPolygon(fromstr(str(the_geom)),)
            else:
                country.geometry = the_geom
            country.save()

class Command(BaseCommand):


    def handle(self, *args, **options):

        import_countries()