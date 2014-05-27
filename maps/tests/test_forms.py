import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from django.core.urlresolvers import reverse

from maps.forms import MapRequestForm
from maps.models import MapSize, Format, Requester
from .testdata import load_test_data


class FormTests(TestCase):

    def setUp(self):
        super(FormTests, self).setUp()

        self.form_data = {
            'title': 'Test request',
            'date': '2013-05-01T22:05:12',
            'email': 's@d.com',
            'user': '/api/users/%s/',
            'format': '/api/formats/%s/',
            'requester': '/api/requesters/%s/',
            'size': '/api/sizes/%s/',
            'deadline': '2014-05-01',
            'quantity': '2'
        }

        load_test_data('maprequests')

        self.post_url = reverse('api_dispatch_list', kwargs={
            'api_name': 'api', 
            'resource_name': 'requests'
        })

    def test_maprequest_form_valid(self):

        self.form_data['user'] = User.objects.all()[0].pk
        self.form_data['size'] = MapSize.objects.all()[0].pk
        self.form_data['format'] = Format.objects.all()[0].pk
        self.form_data['requester'] = Requester.objects.all()[0].pk

        form = MapRequestForm(data=self.form_data)
        self.assertEqual(form.is_valid(), True)

   