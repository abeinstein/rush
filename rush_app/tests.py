"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""
from django.test import TestCase
from tastypie.test import ResourceTestCase
from rush_app.models import UserProfile, Rush, Frat
from django.contrib.auth.models import User


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class FratResourceTest(ResourceTestCase):
    fixtures = ['rush_data.json']

    def setUp(self):
        super(FratResourceTest, self).setUp()

    def test_get_frat(self):
        resp = self.api_client.get('/api/v1/frat/')
        self.assertValidJSONResponse(resp)

        data = self.deserialize(resp)['objects']
        self.assertEqual(len(data), 3)
        aepi = data[0]

        self.assertEqual(aepi["chapter"], "Lambda")
        self.assertEqual(len(aepi["rushes"]), 3)

    def test_basic_subtraction(self):
        """
        Tests that 3 - 1 always equals 2.
        """
        self.assertEqual(3 - 1, 2)

        
