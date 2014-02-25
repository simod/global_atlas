import os

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.core.files import File

from maps.models import CollinsMap, Country

def load_collins():

    with open('data/collins.csv', 'rU') as maps:
        for row in maps.readlines():
            row = row.split(';')
            folder = row[0]
            name = row[1]
            try:
                country = Country.objects.filter(fips=row[2])[0]
            except:
                print 'Missing country with fips = %s' % row[2]
                continue
            try:
                the_file = File(open('collins/%s/%s.png' % (folder, name)))
            except: raise

            try:
                if not CollinsMap.objects.filter(name=name, country = country).exists():
                    coll, created = CollinsMap.objects.get_or_create(
                        name = name,
                        country = country,
                        the_file = the_file
                    )
                    if created: print 'Created map %s' % name
                else:
                    print 'Skipped existing map with name = %s' % name
            except: raise
    print 'Loaded %s maps' % CollinsMap.objects.count()


class Command(BaseCommand):

    def handle(self, *args, **options):

        load_collins()