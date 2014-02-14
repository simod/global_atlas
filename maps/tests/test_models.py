from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.gis.geos import GEOSGeometry

from maps.models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source
from .testdata import load_test_data, samplefile


class ModelsMapTests(TestCase):
    """Test the Map models"""

    def setUp(self):
        load_test_data('maps')

    def test_map_create(self):
        """Test Map create"""
        themap, created = Map.objects.get_or_create(
            title = 'atitle',
            date = datetime.now(),
            theme = Theme.objects.get(slug='crisis'),
            category = Category.objects.get(slug='location'),
            source = Source.objects.get(slug='jrc'),
            center = GEOSGeometry("POINT (0 0)"),
            request = MapRequest.objects.all()[0],
            map_file = samplefile,
            map_thumbnail = samplefile,
            country = Country.objects.get(fips='IT'),
            size = MapSize.objects.get(name='A4')
        )
        self.assertTrue(created)
        self.assertEqual(str(themap),'atitle')

    def test_map_update(self):
        """Test Map update"""
        description = 'other description'
        themap = Map.objects.get(title='A map')
        themap.description = description
        themap.save()
        themap = Map.objects.get(title='A map')
        self.assertEqual(themap.description, description)

    def test_map_delete(self):
        """Test Map delete"""
        Map.objects.get(title='A map').delete()
        maps = Map.objects.filter(title='A map').count()
        self.assertEqual(maps, 0)


class ModelsThemeTests(TestCase):
    """Test the Theme models"""

    def setUp(self):
        load_test_data('themes')

    def test_theme_create(self):
        """Test Theme create"""
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

    def test_theme_slug_create(self):
        """Test Theme Slug is properly sluggified"""
        theme, created = Theme.objects.get_or_create(
            name = u'this is a name',
        )
        self.assertEqual(theme.slug, 'this-is-a-name')

    def test_theme_update(self):
        """Test Theme update"""
        theme = Theme.objects.get(slug='crisis')
        theme.name = 'faketitle'
        theme.save()
        theme = Theme.objects.get(slug='crisis')
        self.assertEqual(theme.name, 'faketitle')

    def test_theme_delete(self):
        """Test Theme delete"""
        Theme.objects.get(slug='crisis').delete()
        themes = Theme.objects.filter(slug='crisis').count()
        self.assertEqual(themes, 0)


class ModelsMapRequestTests(TestCase):
    """Test the MapRequest models"""

    def setUp(self):
        load_test_data('maprequests')

    def test_map_request_create(self):
        """Test MapRequest create"""       
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

    def test_map_request_update(self):
        """Test MapRequest update"""
        mr = MapRequest.objects.all()[0]
        mr.title = 'faketitle'
        mr.save()
        mr = MapRequest.objects.get(pk=mr.pk)
        self.assertEqual(mr.title, 'faketitle')

    def test_map_request_delete(self):
        """Test MapRequest delete"""
        mr = MapRequest.objects.all()[0]
        mr.delete()
        mrs = MapRequest.objects.filter(title=mr.title).count()
        self.assertEqual(mrs, 0)


class ModelsCountryTests(TestCase):
    """Test the Country models"""

    def setUp(self):
        load_test_data('countries')

    def test_country_create(self):
        """Test Country create"""
        co, created = Country.objects.get_or_create(
            fips = 'CO',
            name = 'atlantis'
        )
        co.countries.add(Country.objects.get(fips='IT'))
        co.countries.add(Country.objects.get(fips='NO'))
        self.assertTrue(created)
        self.assertEqual(str(co),'atlantis')

    def test_country_update(self):
        """Test Country update"""
        co = Country.objects.get(fips='IT')
        co.iso2 = 'IK'
        co.save()
        co = Country.objects.get(fips='IT')
        self.assertEqual(co.iso2, 'IK')

    def test_country_delete(self):
        """Test Country delete"""
        Country.objects.get(fips='IT').delete()
        cs = Country.objects.filter(iso2='IT').count()
        self.assertEqual(cs, 0)


class ModelsFormatTests(TestCase):
    """Test the Format models"""

    def setUp(self):
        load_test_data('formats')

    def test_format_create(self):
        """ Test Format create"""
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

    def test_format_update(self):
        """Test Format update"""
        fo = Format.objects.get(name='jpg', resolution='high')
        fo.resolution = 'low'
        fo.save()
        fo = Format.objects.get(pk=fo.pk)
        self.assertEqual(fo.resolution, 'low')

    def test_format_delete(self):
        """Test Format delete"""
        Format.objects.get(name='jpg', resolution='high').delete()
        fs = Format.objects.filter(name='jpg').count()
        self.assertEqual(fs, 0)


class ModelsMapSizeTests(TestCase):
    """Test the MapSize models create"""

    def setUp(self):
        load_test_data('sizes')

    def test_map_size_create(self):
        """Test MapSize create"""
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

    def test_map_size_update(self):
        """Test MapSize update"""
        ms = MapSize.objects.get(name='A4')
        ms.dimensions = '3*3'
        ms.save()
        ms = MapSize.objects.get(pk=ms.pk)
        self.assertEqual(ms.dimensions, '3*3')

    def test_map_size_delete(self):
        """Test MapSize delete"""
        MapSize.objects.get(name='A4').delete()
        ms = MapSize.objects.filter(name='A4').count()
        self.assertEqual(ms, 0)


class ModelsCategoryTests(TestCase):
    """Test the Category models"""

    def setUp(self):
        load_test_data('categories')

    def test_category_create(self):
        """Test Category create"""
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

    def test_category_slug_creation(self):
        """Test Theme Slug creation"""
        cat, created = Category.objects.get_or_create(
            name = u'Biota Category',
        )
        self.assertEqual(cat.slug, 'biota-category')

    def test_category_update(self):
        """Test Category update"""
        cat = Category.objects.get(slug='location')
        cat.name = 'fakename'
        cat.save()
        cat = Category.objects.get(pk=cat.pk)
        self.assertEqual(cat.name, 'fakename')

    def test_category_delete(self):
        """Test Category delete"""
        Category.objects.get(slug='location').delete()
        cs = Category.objects.filter(name='Location').count()
        self.assertEqual(cs, 0)


class ModelsRequesterTests(TestCase):
    """Test the Requester models"""

    def setUp(self):
        load_test_data('requesters')

    def test_requester_create(self):
        """Test Requester create"""
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

    def test_requester_slug_creation(self):
        """Test Requester Slug creation"""
        req, created = Requester.objects.get_or_create(
            name = u'Mr Brown',
        )
        self.assertEqual(req.slug, 'mr-brown')

    def test_requester_update(self):
        """Test Requester update"""
        req = Requester.objects.get(slug='francis')
        req.name = 'Fran'
        req.save()
        req = Requester.objects.get(pk=req.pk)
        self.assertEqual(req.name, 'Fran')

    def test_requester_delete(self):
        """Test Requester delete"""
        Requester.objects.get(slug='francis').delete()
        rs = Requester.objects.filter(name='Francis').count()
        self.assertEqual(rs, 0)


class ModelsSourceTests(TestCase):
    """Test the Source models"""

    def setUp(self):
        load_test_data('sources')

    def test_source_create(self):
        """Test Source create"""
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

    def test_source_slug_creation(self):
        """Test Source Slug creation"""
        so, created = Source.objects.get_or_create(
            name = u'J R C',
        )
        self.assertEqual(so.slug, 'j-r-c')

    def test_source_update(self):
        """Test Source update"""
        so = Source.objects.get(slug='jrc')
        so.name = 'OCHA'
        so.save()
        so = Source.objects.get(pk=so.pk)
        self.assertEqual(so.name, 'OCHA')

    def test_source_delete(self):
        """ Test Source delete"""
        Source.objects.get(slug='jrc').delete()
        ss = Source.objects.filter(name='JRC').count()
        self.assertEqual(ss, 0)


class ModelManagerTests(TestCase):
    """Test the model managers custom methods"""

    def setUp(self):
        load_test_data('countries')

    def test_country_manager_get_regions(self):
        """Test that the get_regions method 
         returns just them"""
        count = Country.objects.get_regions().count()
        self.assertEqual(count, 1)

    def test_country_manager_get_countries(self):
        """Test that the get_countries method
         returns just them"""
        count = Country.objects.get_countries().count()
        self.assertEqual(count, 2)
