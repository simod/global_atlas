from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError

from maps.models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source
from .testdata import loadTestData, samplefile, point

class ModelsCreateTests(TestCase):
    """Test the models creation"""

    def setUp(self):
        loadTestData()

    def testMapCreation(self):
        """Test Map creation"""
        themap, created = Map.objects.get_or_create(
            title = 'atitle',
            date = datetime.now(),
            theme = Theme.objects.get(slug='crisis'),
            category = Category.objects.get(slug='location'),
            source = Source.objects.get(slug='jrc'),
            center = point,
            request = MapRequest.objects.all()[0],
            map_file = samplefile,
            map_thumbnail = samplefile,
            country = Country.objects.get(fips='ITA'),
            size = MapSize.objects.get(name='A4')
        )
        self.assertTrue(created)
        self.assertEqual(str(themap),'atitle')

    def testThemeCreation(self):
        """Test Theme creation"""
        theme, created = Theme.objects.get_or_create(
            name = 'thename',
            slug = 'theslug'
        )
        self.assertTrue(created)
        self.assertEqual(str(theme),'thename')

        try:
            integrity_error = False
            Theme.objects.get_or_create(
                name = 'anothername',
                slug = 'theslug'
            )
        except IntegrityError, e:
            integrity_error = True
        self.assertTrue(integrity_error)

    def testThemeSlugCreation(self):
        """Test Theme Slug creation"""
        theme, created = Theme.objects.get_or_create(
            name = u'this is a name',
        )
        self.assertEqual(theme.slug, 'this-is-a-name')

    def testMapRequestCreation(self):
        """Test MapRequest creation"""       
        mr, created = MapRequest.objects.get_or_create(
            title = 'title',
            email = 's@d.com',
            user = User.objects.get(username='simone'),
            date = datetime.now(),
            size = MapSize.objects.get(name='A4'),
            format = Format.objects.filter(name='pdf')[0],
            requester = Requester.objects.get(slug='francis')
        )
        self.assertTrue(created)
        self.assertEqual(str(mr),'title')

    def testCountryCreation(self):
        """Test Country creation"""
        co, created = Country.objects.get_or_create(
            fips = 'COUNT',
            name = 'atlantis'
        )
        co.countries.add(Country.objects.get(fips='ITA'))
        co.countries.add(Country.objects.get(fips='NOR'))
        self.assertTrue(created)
        self.assertEqual(str(co),'atlantis')

    def testFormatCreation(self):
        """ Test Format creation"""
        fo, created = Format.objects.get_or_create(
            name = 'gif',
            resolution = 'low'
        )
        self.assertTrue(created)
        self.assertEqual(str(fo),'gif - low')

        #test creating an existing format raises an error
        try:
            integrity_error = False
            Format.objects.create(
                name = 'jpg',
                resolution = 'high'
            )
        except IntegrityError, e:
            integrity_error = True
        self.assertTrue(integrity_error)

    def testMapSizeCreation(self):
        """Test MapSize creation"""
        ms, created = MapSize.objects.get_or_create(
            name = 'A2',
            dimensions = '34*35'
        )
        self.assertTrue(created)
        self.assertEqual(str(ms),'A2')

        #test creating an existing size raises an error
        try:
            integrity_error = False
            MapSize.objects.create(
                name = 'A4',
                dimensions = '34*35'
            )
        except IntegrityError, e:
            integrity_error = True
        self.assertTrue(integrity_error)

    def testCategoryCreation(self):
        """Test Category creation"""
        cat, created = Category.objects.get_or_create(
            name = 'Biota',
            slug = 'biota'
        )
        self.assertTrue(created)
        self.assertEqual(str(cat),'Biota')

        #test creating an existing category raises an error
        try:
            integrity_error = False
            Category.objects.create(
                name = 'Crisis',
                slug = 'crisis'
            )
        except IntegrityError, e:
            integrity_error = True
        self.assertTrue(integrity_error)

    def testCategorySlugCreation(self):
        """Test Theme Slug creation"""
        cat, created = Category.objects.get_or_create(
            name = u'Biota Category',
        )
        self.assertEqual(cat.slug, 'biota-category')

    def testRequesterCreation(self):
        """Test Requester creation"""
        req, created = Requester.objects.get_or_create(
            name = 'Simon',
            slug = 'simon'
        )
        self.assertTrue(created)
        self.assertEqual(str(req),'Simon')

        #test creating an existing requester raises an error
        try:
            integrity_error = False
            Requester.objects.create(
                name = 'Francis',
                slug = 'francis'
            )
        except IntegrityError, e:
            integrity_error = True
        self.assertTrue(integrity_error)

    def testRequesterSlugCreation(self):
        """Test Requester Slug creation"""
        req, created = Requester.objects.get_or_create(
            name = u'Mr Brown',
        )
        self.assertEqual(req.slug, 'mr-brown')   

    def testSourceCreation(self):
        """Test Source creation"""
        so, created = Source.objects.get_or_create(
            name = 'AAA',
            slug = 'aaa'
        ) 
        self.assertTrue(created)
        self.assertEqual(str(so),'AAA')

        #test creating an existing source raises an error
        try:
            integrity_error = False
            Source.objects.create(
                name = 'JRC',
                slug = 'jrc'
            )
        except IntegrityError, e:
            integrity_error = True
        self.assertTrue(integrity_error)

    def testSourceSlugCreation(self):
        """Test Source Slug creation"""
        so, created = Source.objects.get_or_create(
            name = u'J R C',
        )
        self.assertEqual(so.slug, 'j-r-c')


class ModelsUpdateTests(TestCase):
    """Test the models update"""

    def setUp(self):
        loadTestData()

    def testMapUpdate(self):
        """Test Map update"""
        description = 'other description'
        themap = Map.objects.get(title='A map')
        themap.description = description
        themap.save()
        themap = Map.objects.get(title='A map')
        self.assertEqual(themap.description, description)

    def testThemeUpdate(self):
        """Test Theme update"""
        theme = Theme.objects.get(slug='crisis')
        theme.name = 'faketitle'
        theme.save()
        theme = Theme.objects.get(slug='crisis')
        self.assertEqual(theme.name, 'faketitle')

    def testMapRequestUpdate(self):
        """Test MapRequest update"""
        mr = MapRequest.objects.all()[0]
        mr.title = 'faketitle'
        mr.save()
        mr = MapRequest.objects.get(pk=mr.pk)
        self.assertEqual(mr.title, 'faketitle')

    def testCountryUpdate(self):
        """Test Country update"""
        co = Country.objects.get(fips='ITA')
        co.iso2 = 'IK'
        co.save()
        co = Country.objects.get(fips='ITA')
        self.assertEqual(co.iso2, 'IK')

    def testFormatUpdate(self):
        """Test Format update"""
        fo = Format.objects.get(name='jpg', resolution='high')
        fo.resolution = 'low'
        fo.save()
        fo = Format.objects.get(pk=fo.pk)
        self.assertEqual(fo.resolution, 'low')

    def testMapSizeUpdate(self):
        """Test MapSize update"""
        ms = MapSize.objects.get(name='A4')
        ms.dimensions = '3*3'
        ms.save()
        ms = MapSize.objects.get(pk=ms.pk)
        self.assertEqual(ms.dimensions, '3*3')

    def testCategoryUpdate(self):
        """Test Category update"""
        cat = Category.objects.get(slug='location')
        cat.name = 'fakename'
        cat.save()
        cat = Category.objects.get(pk=cat.pk)
        self.assertEqual(cat.name, 'fakename')

    def testRequesterUpdate(self):
        """Test Requester update"""
        req = Requester.objects.get(slug='francis')
        req.name = 'Fran'
        req.save()
        req = Requester.objects.get(pk=req.pk)
        self.assertEqual(req.name, 'Fran')

    def testSourceUpdate(self):
        """Test Source update"""
        so = Source.objects.get(slug='jrc')
        so.name = 'OCHA'
        so.save()
        so = Source.objects.get(pk=so.pk)
        self.assertEqual(so.name, 'OCHA')

class ModelsDeleteTests(TestCase):
    """Test the models deletion"""

    def setUp(self):
        loadTestData()

    def testMapDelete(self):
        """Test Map delete"""
        Map.objects.get(title='A map').delete()
        maps = Map.objects.filter(title='A map').count()
        self.assertEqual(maps, 0)

    def testThemeDelete(self):
        """Test Theme delete"""
        Theme.objects.get(slug='crisis').delete()
        themes = Theme.objects.filter(slug='crisis').count()
        self.assertEqual(themes, 0)

    def testMapRequestDelete(self):
        """Test MapRequest delete"""
        mr = MapRequest.objects.all()[0]
        mr.delete()
        mrs = MapRequest.objects.filter(title=mr.title).count()
        self.assertEqual(mrs, 0)

    def testCountryDelete(self):
        """Test Country delete"""
        Country.objects.get(fips='ITA').delete()
        cs = Country.objects.filter(iso2='IT').count()
        self.assertEqual(cs, 0)

    def testFormatDelete(self):
        """Test Format delete"""
        Format.objects.get(name='jpg', resolution='high').delete()
        fs = Format.objects.filter(name='jpg').count()
        self.assertEqual(fs, 0)

    def testMapSizeDelete(self):
        """Test MapSize delete"""
        MapSize.objects.get(name='A4').delete()
        ms = MapSize.objects.filter(name='A4').count()
        self.assertEqual(ms, 0)

    def testCategoryDelete(self):
        """Test Category delete"""
        Category.objects.get(slug='location').delete()
        cs = Category.objects.filter(name='Location').count()
        self.assertEqual(cs, 0)

    def testRequesterDelete(self):
        """Test Requester delete"""
        Requester.objects.get(slug='francis').delete()
        rs = Requester.objects.filter(name='Francis').count()
        self.assertEqual(rs, 0)

    def testSourceDelete(self):
        """ Test Source delete"""
        Source.objects.get(slug='jrc').delete()
        ss = Source.objects.filter(name='JRC').count()
        self.assertEqual(ss, 0)
