from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from django.test import LiveServerTestCase
from django.contrib.auth.models import User

from rush_app.models import Frat

class ChromeTests(LiveServerTestCase):
    fixtures = ['rush_fixture.json']

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def abs_url(self, path):
        return self.live_server_url + path

    def fill_out_signup_form(self, data):
        ''' Accepts a dictionary of {<element_id>: <value>} pairs,
        and fills out a form. 
        Doesn't submit the form.
        '''
        if 'signup' not in self.browser.current_url:
            self.browser.get(self.abs_url('/signup'))
        for key, val in data.iteritems():
            if key in ['id_school', 'id_frat']:
                select = Select(self.browser.find_element_by_id(key))
                select.select_by_visible_text(val)
            else:
                elem = self.browser.find_element_by_id(key)
                elem.send_keys(val)

class HomePageTests(ChromeTests):
    def test_visit_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Rush: Go Greek', self.browser.title)

class LoginTests(ChromeTests):

    def test_existing_user_login(self):
        self.browser.get(self.abs_url('/login'))
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys("slewis")
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys("password")
        password_field.submit()

        self.assertIn("rushes", self.browser.current_url)

    def test_non_existing_user_login(self):
        self.browser.get(self.abs_url('/login'))
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys("non_existing_user")
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys("invalid_password")
        password_field.submit()

        self.assertNotEqual(self.browser.current_url, self.abs_url("/rushes"))
        self.assertEqual(self.browser.find_element_by_id('login_error').text, 
            "Sorry, not a valid username or password. Please try again.")
        self.assertIn("login", self.browser.current_url)

class SignupTests(ChromeTests):


    def submit(self):
        self.browser.find_element_by_id("submit-button").click()

    def test_new_frat_signup(self):
        # Ensure frat does not exist
        self.assertFalse(Frat.objects.filter(name="Psi Upsilon", university="University of Chicago").exists())
        self.assertFalse(User.objects.filter(username="jsmith").exists())    

        self.browser.get(self.abs_url("/signup"))
        self.browser.find_element_by_id("new_frat").click()
        data = {
            'id_first_name': 'John',
            'id_last_name': 'Smith',
            'id_email': "jsmith@email.com",
            'id_username': 'jsmith',
            'id_password': 'password',
            'id_password_confirmation': 'password',
            'id_frat_password': 'fratpassword',
            'id_frat_password_confirmation': 'fratpassword',
            'id_school': "University of Chicago",
            'id_frat': "Psi Upsilon"
        }
        self.fill_out_signup_form(data)

        self.submit()
        
        self.assertIn("rushes", self.browser.current_url)
        self.assertTrue(Frat.objects.filter(name="Psi Upsilon", university="University of Chicago").exists())
        self.assertTrue(User.objects.filter(username="jsmith").exists())

    def test_existing_frat_signup(self):
        self.assertTrue(Frat.objects.filter(name="Alpha Epsilon Pi", university="University of Chicago").exists())
        self.assertFalse(User.objects.filter(username="tsvibt").exists())

        self.browser.get(self.abs_url("/signup"))
        self.browser.find_element_by_id("existing_frat").click()
        data = {
            'id_first_name': 'Tsvi',
            'id_last_name': 'Benson-Tilsen',
            'id_email': "tsvibt@email.com",
            'id_username': 'tsvibt',
            'id_password': 'password',
            'id_password_confirmation': 'password',
            'id_frat_password': 'password',
            'id_school': "University of Chicago",
            'id_frat': "Alpha Epsilon Pi"
        }
        self.fill_out_signup_form(data)

        self.submit()

        self.assertIn("rushes", self.browser.current_url)
        self.assertTrue(User.objects.filter(username="tsvibt").exists())

class BehaviorTests(ChromeTests):
    def submit(self):
        self.browser.find_element_by_id("submit-button").click()

    def test_two_users_signup_one_after_another(self):
        self.assertFalse(frat_exists("Delta Upsilon", "University of Chicago"))
        self.assertFalse(user_exists("user1"))
        self.assertFalse(user_exists("user2"))

        self.browser.get(self.abs_url("/signup"))
        self.browser.find_element_by_id("new_frat").click()

        data_user1 = {
            'id_first_name': 'User1',
            'id_last_name': 'User1',
            'id_email': "user1@email.com",
            'id_username': 'user1',
            'id_password': 'password',
            'id_password_confirmation': 'password',
            'id_frat_password': 'password',
            'id_frat_password_confirmation': 'password',
            'id_school': "University of Chicago",
            'id_frat': "Delta Upsilon"
        }
        self.fill_out_signup_form(data_user1)
        self.submit()

        self.assertIn("rushes", self.browser.current_url)
        self.assertTrue(user_exists("user1"))
        self.assertTrue(frat_exists("Delta Upsilon", "University of Chicago"))

        self.browser.get(self.abs_url("/logout"))

        self.assertEqual(self.browser.current_url, self.abs_url('/'))

        self.browser.get(self.abs_url("/signup"))
        self.browser.find_element_by_id("existing_frat").click()

        data_user2 = {
            'id_first_name': 'User2',
            'id_last_name': 'User2',
            'id_email': "user2@email.com",
            'id_username': 'user2',
            'id_password': 'password',
            'id_password_confirmation': 'password',
            'id_frat_password': 'password',
            'id_school': "University of Chicago",
            'id_frat': "Delta Upsilon"
        }

        self.fill_out_signup_form(data_user2)
        self.submit()
        
        self.assertIn("rushes", self.browser.current_url)
        self.assertTrue(user_exists("user2"))







def frat_exists(name, school):
    return Frat.objects.filter(name=name, university=school).exists()

def user_exists(username):
    return User.objects.filter(username=username).exists()


