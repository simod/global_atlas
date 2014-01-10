from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from maps.models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source
from maps.admin import ThemeAdmin, CategoryAdmin, RequesterAdmin, SourceAdmin, \
    CountryAdmin

class AdminTests(TestCase):

    def test_source_admin(self):
        """Test SourceAdmin prepopupated fields"""
        sa = SourceAdmin(Source, AdminSite())
        self.assertTrue('slug' in sa.prepopulated_fields)

    def test_theme_admin(self):
        """Test ThemeAdmin prepopupated fields"""
        ta = ThemeAdmin(Theme, AdminSite())
        self.assertTrue('slug' in ta.prepopulated_fields)

    def test_requester_admin(self):
        """Test RequesterAdmin prepopupated fields"""
        ra = RequesterAdmin(Requester, AdminSite())
        self.assertTrue('slug' in ra.prepopulated_fields)

    def test_category_admin(self):
        """Test CategoryAdmin prepopupated fields"""
        ca = CategoryAdmin(Category, AdminSite())
        self.assertTrue('slug' in ca.prepopulated_fields)

    def test_country_admin(self):
        """Test CategoryAdmin filter fields"""
        ca = CountryAdmin(Country, AdminSite())
        self.assertTrue('countries' in ca.filter_horizontal)