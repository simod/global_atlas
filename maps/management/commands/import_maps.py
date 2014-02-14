import os

from datetime import datetime

from django.contrib.gis.geos import Point
from django.utils.text import slugify

from maps.models import Country, Map, MapRequest, Theme, Category, \
    Source, MapSize

"""
Bulk load existing maps from a csv file
structured as:
Map_ID;TITLE;FIPS;COUNTRY;MAP SIZE;DATE;THEME;CATEGORY;SOURCE;DESC;MAP SCALE;WHO;FILENAME;LONG;LAT
"""

def load_maps():

    with open('../../../data/MAPS2.csv', 'rU') as maps:
        for row in maps.read():
            row = row.split(';')
            id = row[0]
            title = row[1]
            country = Country.objects.filter(fips=row[2])[0]
            size = MapSize.objects.get_or_create(name=row[4].split('(')[0])
            date = datetime.strptime(row[5], '%d/%m/%y')
            theme = Theme.objects.get_or_create(name=row[6], slug=slugify(row[6]))
            category = Category.objects.get_or_create(name=row[7], slug=slugify(row[7]))
            source = Source.objects.get_or_create(name=row[8], slug=slugify(row[8]))
            description = row[9]
            scale = row[10]
            maprequest = MapRequest.objects.filter(requester__name=row[11])[0]
            map_file = open('../../../uploads/maps/%s' % row[12])
            map_thumbnail = open('../../../static_root/thumbnails/%s' % '%s.jpg' 
                % os.path.splitext(row[12])[0])
            center = Point(float(row[13].replace(',','.')), 
                float(row[14].replace(',','.')))

            try:
                themap = Map.objects.get_or_create(
                    pk = id,
                    title = title,
                    country = country,
                    size = size,
                    date = date,
                    theme = theme,
                    category = category,
                    source = source,
                    description = description,
                    scale = scale,
                    request = maprequest,
                    center = center,
                    map_file = map_file,
                    map_thumbnail = map_thumbnail
                )
            except: raise
    print 'Loaded %s maps' % Map.objects.count()

class Command(BaseCommand):

    def handle(self, *args, **options):

        load_maps()
