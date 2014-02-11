from selenium import webdriver
import unittest

class ChromeTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

class HomePageTests(ChromeTests):
    def test_visit_home_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Rush: Go Greek', self.browser.title)

class LoginTests(ChromeTests):
    def test_existing_user_login(self):
        self.browser.get('http://localhost:8000/login')
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys("slewis")
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys("password")
        password_field.submit()

        self.assertEqual(self.browser.current_url, "http://localhost:8000/rushes/")
        self.assertIn("rushes", self.browser.current_url)

    def test_non_existing_user_login(self):
        self.browser.get('http://localhost:8000/login')
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys("non_existing_user")
        password_field = self.browser.find_element_by_id('id_password')
        password_field.send_keys("invalid_password")
        password_field.submit()

        self.assertNotEqual(self.browser.current_url, "http://localhost:8000/rushes/")
        self.assertEqual(self.browser.find_element_by_id('login_error').text, 
            "Sorry, not a valid username or password. Please try again.")
        self.assertIn("signup", self.browser.current_url)


if __name__ == '__main__':
    unittest.main()