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

    def setUp(self):
        super(MapApiTests, self).setUp()

        load_test_data()
        self.url = '/api/maps/'

    def test_map_list_unauthorized(self):
        self.assertHttpUnauthorized(self.api_client.get(self.url))

    def test_valid_json_response(self):
        self.api_client.client.login(username=username, password=password)
        resp = self.api_client.get(self.url)
        self.assertValidJSONResponse(resp)

        self.assertEquals(len(self.deserialize(resp)['objects']), 2)