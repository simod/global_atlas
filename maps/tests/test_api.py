import datetime

from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

from maps.models import Map, Theme, MapRequest, Country, Format, \
    MapSize, Category, Requester, Source
from .testdata import load_test_data

username = 'simone'
password = 'thepwd'



class MapApiTests(ResourceTestCase):
    """Tests the Maps apis"""

    def get_credentials(self):
        return self.create_basic(username=username, password=password)

    def setUp(self):
        super(MapApiTests, self).setUp()

        load_test_data()
        self.url = '/api/maps/'

    def test_map_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.url))

    def test_map_list_authorized(self):
        resp = self.api_client.get(self.url,  
            authentication=self.get_credentials())