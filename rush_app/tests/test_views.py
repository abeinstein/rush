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

    def test_signup_new_frat(self):
        self.assertFalse(Frat.objects.filter(name="Psi Upsilon", university="Amherst College").exists())

        data = {
            'new_frat_created': True,
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'jsmith@mail.com',
            'username': 'jsmith',
            'password': 'password',
            'password_confirmation': 'password',
            'frat': 'Psi Upsilon',
            'school': 'Amherst College',
            'frat_password': 'fratpassword',
            'frat_password_confirmation': 'fratpassword'
        }

        resp = self.client.post('/signup', data)
        self.assertEqual(resp.status_code, 301)

        self.assertTrue(Frat.objects.filter(name="Psi Upsilon", university="Amherst College").exists())



