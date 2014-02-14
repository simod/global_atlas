import os

from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from django.utils.text import slugify
from django.core.files import File

from maps.models import Country, Map, MapRequest, Theme, Category, \
    Source, MapSize

"""
Bulk load existing maps from a csv file
structured as:
Map_ID;TITLE;FIPS;COUNTRY;MAP SIZE;DATE;THEME;CATEGORY;SOURCE;DESC;MAP SCALE;
WHO;FILENAME;LONG;LAT
"""

def load_maps():

    with open('data/MAPS2.csv', 'rU') as maps:
        for row in maps.readlines():
            row = row.split(';')
            id = int(row[0])
            title = row[1]
            try:
                country = Country.objects.filter(fips=row[2])[0]
            except:
                print 'Missing country with fips = %s' % row[2]
                raise
            size, c = MapSize.objects.get_or_create(name=row[4].split('(')[0])
            date = datetime.strptime(row[5], '%d/%m/%y')
            theme, c = Theme.objects.get_or_create(name=row[6], 
                slug=slugify(unicode(row[6])))
            category, c = Category.objects.get_or_create(name=row[7], 
                slug=slugify(unicode(row[7])))
            source, c = Source.objects.get_or_create(name=row[8], 
                slug=slugify(unicode(row[8])))
            description = row[9]
            scale = row[10]
            maprequest = MapRequest.objects.get(title='initial')
            try:
                map_file = File(open('maps/%s' % row[12]))
            except: raise
            try:
                map_thumbnail = File(open('thumbnails/%s' % '%s.jpg' 
                    % os.path.splitext(row[12])[0]))
            except:
                print 'Thumbnail for file %s not found' % row[12]
                map_thumbnail = None
                continue

            try:
                center = Point(float(row[13].replace(',','.')), 
                float(row[14].replace(',','.')))
            except: 
                center = None
                continue

            try:
                themap, created = Map.objects.get_or_create(
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
                if created:
                    print 'Saved maps with id %s' % themap.pk
                else: print 'Updated maps with id %s' % themap.pk

            except: raise
    print 'Loaded %s maps' % Map.objects.count()

class Command(BaseCommand):

    def handle(self, *args, **options):

        load_maps()
