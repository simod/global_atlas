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

        load_test_data('maps')
        self.list_url = '/api/maps/'
        self.detail_url = '/api/maps/%s/'

    def test_map_get_list_unauth(self):
        """Test that a 401 is given when unauth"""
        self.assertHttpUnauthorized(self.api_client.get(
            self.list_url))

    def test_map_get_list(self):
        """Test that a valid json response is given
        and the count is 2"""
        self.api_client.client.login(username=username, password=password)
        resp = self.api_client.get(self.list_url)
        self.assertValidJSONResponse(resp)

        self.assertEquals(len(self.deserialize(resp)['objects']), 2)

    def test_map_get_detail_unauth(self):
        """Test that a 401 is given on detail view when unath"""
        themap = Map.objects.all()[0]
        self.assertHttpUnauthorized(
            self.api_client.get(self.detail_url % themap.pk))

    def test_map_get_detail(self):
        """Test that a valid map detail is returned when authenticated"""
        self.api_client.client.login(username=username, password=password)
        themap = Map.objects.all()[0]
        resp = self.api_client.get(self.detail_url % themap.pk)
        self.assertValidJSONResponse(resp)

        self.assertKeys(self.deserialize(resp), [u'category', u'scale', 
            u'title',  u'description', u'country', u'request', u'source', 
            u'theme', u'map_thumbnail', u'date', u'size', u'map_file', u'center',
            u'id', u'resource_uri'])
        self.assertEqual(self.deserialize(resp)['title'], 'A map')

    def test_map_post_unauth(self):
        """Test that 401 on unauthenticated post"""
        self.assertHttpUnauthorized(self.api_client.post(self.list_url, 
            data={}))

    def test_map_post(self):
        """Test a map post while authenticated"""
        self.assertEqual(Map.objects.count(), 2)
        post_data = {
            'title': 'Test map',
            'date': '2013-05-01T22:05:12',
            'theme': '/api/themes/%s/' % Theme.objects.all()[0].pk,
            'category': '/api/categories/%s/' % Category.objects.all()[0].pk,
            'source': '/api/sources/%s/' % Source.objects.all()[0].pk,
            'request': '/api/requests/%s/' % MapRequest.objects.all()[0].pk,
            'country': '/api/countries/%s/' % Country.objects.all()[0].pk,
            'size': '/api/sizes/%s/' % MapSize.objects.all()[0].pk,
            'map_file': 'uploads/thumbnails/test.gif',
            'map_thumbnail': 'uploads/thumbnails/test.gif'
        }
        self.api_client.client.login(username=username, password=password)
        self.assertHttpCreated(self.api_client.post(self.list_url, 
            format='json', data=post_data))
        self.assertEqual(Map.objects.count(), 3)

    def test_map_put_unauth(self):
        """Test that 401 on unauthenticated put"""
        self.assertHttpUnauthorized(self.api_client.put(self.list_url, 
            data={}))

    def test_map_put(self):
        """Test a map put while authenticated"""
        themap = Map.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        themap_data = self.deserialize(self.api_client.get(
            self.detail_url % themap.pk))
        new_data = themap_data.copy()
        new_data['title'] = 'Updated title'

        self.assertEqual(Map.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(
            self.detail_url % themap.pk, format='json', data=new_data))
        self.assertEqual(Map.objects.count(), 2)

        self.assertEqual(Map.objects.get(pk=themap.pk).title, 'Updated title')

    def test_map_delete_unauth(self):
        """Test that 401 on unauthenticated delete"""
        self.assertHttpUnauthorized(self.api_client.delete(
            self.detail_url % 1, format='json'))

    def test_map_delete(self):
        """Test a map delete while authenticated"""
        self.assertEqual(Map.objects.count(), 2)
        themap = Map.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        self.assertHttpAccepted(self.api_client.delete(
            self.detail_url % themap.pk, format='json'))
        self.assertEqual(Map.objects.count(), 1)


class ThemeApiTests(ResourceTestCase):
    """Tests the Theme apis"""

    def setUp(self):
        super(ThemeApiTests, self).setUp()

        load_test_data('themes')
        self.list_url = '/api/themes/'
        self.detail_url = '/api/themes/%s/'

    def test_theme_get_list_unauth(self):
        """Test that a 401 is given when unauth"""
        self.assertHttpUnauthorized(self.api_client.get(
            self.list_url))

    def test_theme_get_list(self):
        """Test that a valid json response is given
        and the count is 2"""
        self.api_client.client.login(username=username, password=password)
        resp = self.api_client.get(self.list_url)
        self.assertValidJSONResponse(resp)

        self.assertEquals(len(self.deserialize(resp)['objects']), 2)

    def test_theme_get_detail_unauth(self):
        """Test that a 401 is given on detail view when unath"""
        theme = Theme.objects.all()[0]
        self.assertHttpUnauthorized(
            self.api_client.get(self.detail_url % theme.pk))

    def test_theme_get_detail(self):
        """Test that a valid theme detail is returned when authenticated"""
        self.api_client.client.login(username=username, password=password)
        theme = Theme.objects.all()[0]
        resp = self.api_client.get(self.detail_url % theme.pk)
        self.assertValidJSONResponse(resp)

        self.assertKeys(self.deserialize(resp), [u'id', u'name', 
            u'slug', u'resource_uri'])
        self.assertEqual(self.deserialize(resp)['slug'], 'crisis')

    def test_theme_post_unauth(self):
        """Test that 401 on unauthenticated post"""
        self.assertHttpUnauthorized(self.api_client.post(self.list_url, 
            data={}))

    def test_theme_post(self):
        """Test a post while authenticated"""
        self.assertEqual(Theme.objects.count(), 2)
        post_data = {
            'name': 'Conflic',
            'slug': 'conflict'
        }
        self.api_client.client.login(username=username, password=password)
        self.assertHttpCreated(self.api_client.post(self.list_url, 
            format='json', data=post_data))
        self.assertEqual(Theme.objects.count(), 3)

    def test_theme_put_unauth(self):
        """Test that 401 on unauthenticated put"""
        self.assertHttpUnauthorized(self.api_client.put(self.list_url, 
            data={}))

    def test_theme_put(self):
        """Test a put while authenticated"""
        theme = Theme.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        theme_data = self.deserialize(self.api_client.get(
            self.detail_url % theme.pk))
        new_data = theme_data.copy()
        new_data['name'] = 'Updated name'

        self.assertEqual(Theme.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(
            self.detail_url % theme.pk, format='json', data=new_data))
        self.assertEqual(Theme.objects.count(), 2)

        self.assertEqual(Theme.objects.get(pk=theme.pk).name, 'Updated name')

    def test_theme_delete_unauth(self):
        """Test that 401 on unauthenticated delete"""
        self.assertHttpUnauthorized(self.api_client.delete(
            self.detail_url % 1, format='json'))

    def test_theme_delete(self):
        """Test a theme delete while authenticated"""
        self.assertEqual(Theme.objects.count(), 2)
        theme = Theme.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        self.assertHttpAccepted(self.api_client.delete(
            self.detail_url % theme.pk, format='json'))
        self.assertEqual(Theme.objects.count(), 1)


class MapRequestApiTests(ResourceTestCase):
    """Tests the MapRequest apis"""

    def setUp(self):
        super(MapRequestApiTests, self).setUp()

        load_test_data('maprequests')
        self.list_url = '/api/requests/'
        self.detail_url = '/api/requests/%s/'

    def test_maprequest_get_list_unauth(self):
        """Test that a 401 is given when unauth"""
        self.assertHttpUnauthorized(self.api_client.get(
            self.list_url))

    def test_maprequest_get_list(self):
        """Test that a valid json response is given
        and the count is 2"""
        self.api_client.client.login(username=username, password=password)
        resp = self.api_client.get(self.list_url)
        self.assertValidJSONResponse(resp)

        self.assertEquals(len(self.deserialize(resp)['objects']), 2)

    def test_maprequest_get_detail_unauth(self):
        """Test that a 401 is given on detail view when unath"""
        maprequest = MapRequest.objects.all()[0]
        self.assertHttpUnauthorized(
            self.api_client.get(self.detail_url % maprequest.pk))

    def test_maprequest_get_detail(self):
        """Test that a valid maprequest detail is returned when authenticated"""
        self.api_client.client.login(username=username, password=password)
        maprequest = MapRequest.objects.all()[0]
        resp = self.api_client.get(self.detail_url % maprequest.pk)
        self.assertValidJSONResponse(resp)

        self.assertKeys(self.deserialize(resp), [u'id', u'title', 
            u'email', u'user', u'date', u'purpose', u'extended_description', 
            u'content', u'size', u'format', u'requester', u'resource_uri'])
        self.assertEqual(self.deserialize(resp)['title'], 'request1')

    def test_maprequest_post_unauth(self):
        """Test that 401 on unauthenticated post"""
        self.assertHttpUnauthorized(self.api_client.post(self.list_url, 
            data={}))

    def test_maprequest_post(self):
        """Test a post while authenticated"""
        self.assertEqual(MapRequest.objects.count(), 2)
        post_data = {
            'title': 'Test request',
            'date': '2013-05-01T22:05:12',
            'email': 's@d.com',
            'user': '/api/users/%s/' % User.objects.all()[0].pk,
            'format': '/api/formats/%s/' % Format.objects.all()[0].pk,
            'requester': '/api/requesters/%s/' % Requester.objects.all()[0].pk,
            'size': '/api/sizes/%s/' % MapSize.objects.all()[0].pk
        }
        self.api_client.client.login(username=username, password=password)
        self.assertHttpCreated(self.api_client.post(self.list_url, 
            format='json', data=post_data))
        self.assertEqual(MapRequest.objects.count(), 3)

    def test_maprequest_put_unauth(self):
        """Test that 401 on unauthenticated put"""
        self.assertHttpUnauthorized(self.api_client.put(self.list_url, 
            data={}))

    def test_maprequest_put(self):
        """Test a put while authenticated"""
        maprequest = MapRequest.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        maprequest_data = self.deserialize(self.api_client.get(
            self.detail_url % maprequest.pk))
        new_data = maprequest_data.copy()
        new_data['title'] = 'Updated title'

        self.assertEqual(MapRequest.objects.count(), 2)
        self.assertHttpAccepted(self.api_client.put(
            self.detail_url % maprequest.pk, format='json', data=new_data))
        self.assertEqual(MapRequest.objects.count(), 2)

        self.assertEqual(MapRequest.objects.get(pk=maprequest.pk).title, 
            'Updated title')

    def test_maprequest_delete_unauth(self):
        """Test that 401 on unauthenticated delete"""
        self.assertHttpUnauthorized(self.api_client.delete(
            self.detail_url % 1, format='json'))

    def test_maprequest_delete(self):
        """Test a delete while authenticated"""
        self.assertEqual(MapRequest.objects.count(), 2)
        maprequest = MapRequest.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        self.assertHttpAccepted(self.api_client.delete(
            self.detail_url % maprequest.pk, format='json'))
        self.assertEqual(MapRequest.objects.count(), 1)


class CountryApiTests(ResourceTestCase):
    """Tests the Country apis"""

    def setUp(self):
        super(CountryApiTests, self).setUp()

        load_test_data('countries')
        self.list_url = '/api/countries/'
        self.detail_url = '/api/countries/%s/'

    def test_country_get_list_unauth(self):
        """Test that a 401 is given when unauth"""
        self.assertHttpUnauthorized(self.api_client.get(
            self.list_url))

    def test_country_get_list(self):
        """Test that a valid json response is given
        and the count is 2"""
        self.api_client.client.login(username=username, password=password)
        resp = self.api_client.get(self.list_url)
        self.assertValidJSONResponse(resp)

        self.assertEquals(len(self.deserialize(resp)['objects']), 3)

    def test_country_get_detail_unauth(self):
        """Test that a 401 is given on detail view when unath"""
        co = Country.objects.all()[0]
        self.assertHttpUnauthorized(
            self.api_client.get(self.detail_url % co.pk))

    def test_country_get_detail(self):
        """Test that a valid country detail is returned when authenticated"""
        self.api_client.client.login(username=username, password=password)
        co = Country.objects.all()[0]
        resp = self.api_client.get(self.detail_url % co.pk)
        self.assertValidJSONResponse(resp)

        self.assertKeys(self.deserialize(resp), [u'id', u'fips', 
            u'name', u'iso2', u'iso3', u'resource_uri'])
        self.assertEqual(self.deserialize(resp)['fips'], 'ITA')

    def test_country_post_unauth(self):
        """Test that 401 on unauthenticated post"""
        self.assertHttpUnauthorized(self.api_client.post(self.list_url, 
            data={}))

    def test_country_post(self):
        """Test a post while authenticated"""
        self.assertEqual(Country.objects.count(), 3)
        post_data = {
            'fips': 'SPAIN',
            'name': 'Spain',
            'iso2': 'SP',
            'iso3': 'SPA',
            'countries': [
                '/api/countries/%s/' % Country.objects.all()[0],
                '/api/countries/%s/' % Country.objects.all()[1]
            ] 
        }
        self.api_client.client.login(username=username, password=password)
        self.assertHttpCreated(self.api_client.post(self.list_url, 
            format='json', data=post_data))
        self.assertEqual(Country.objects.count(), 4)

    def test_country_put_unauth(self):
        """Test that 401 on unauthenticated put"""
        self.assertHttpUnauthorized(self.api_client.put(self.list_url, 
            data={}))

    def test_country_put(self):
        """Test a put while authenticated"""
        co = Country.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        co_data = self.deserialize(self.api_client.get(
            self.detail_url % co.pk))
        new_data = co_data.copy()
        new_data['fips'] = 'ESPA'

        self.assertEqual(Country.objects.count(), 3)
        self.assertHttpAccepted(self.api_client.put(
            self.detail_url % co.pk, format='json', data=new_data))
        self.assertEqual(Country.objects.count(), 3)

        self.assertEqual(Country.objects.get(pk=co.pk).fips, 
            'ESPA')

    def test_country_delete_unauth(self):
        """Test that 401 on unauthenticated delete"""
        self.assertHttpUnauthorized(self.api_client.delete(
            self.detail_url % 1, format='json'))

    def test_country_delete(self):
        """Test a delete while authenticated"""
        self.assertEqual(Country.objects.count(), 3)
        co = Country.objects.all()[0]
        self.api_client.client.login(username=username, password=password)
        self.assertHttpAccepted(self.api_client.delete(
            self.detail_url % co.pk, format='json'))
        self.assertEqual(Country.objects.count(), 2)

