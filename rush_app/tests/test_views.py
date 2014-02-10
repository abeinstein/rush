from django.test import TestCase

class RushViewsTestCase(TestCase):
    fixtures = ['rush_fixture.json']

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        login_success = self.client.login(username='slewis', password='password')
        self.assertTrue(login_success)

    def test_signup_new_frat(self):
        self.assertTrue(False)

