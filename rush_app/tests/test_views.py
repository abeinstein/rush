from django.test import TestCase

from rush_app.models import Frat

class RushViewsTestCase(TestCase):
    fixtures = ['rush_fixture.json']

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        login_success = self.client.login(username='slewis', password='password')
        self.assertTrue(login_success)



