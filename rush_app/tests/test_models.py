import Image
import os

from django.test import TestCase

from rush_app.models import Frat, Rush

class RushTests(TestCase):
    def setUp(self):
        super(RushTests, self).setUp()

        # Create a frat
        self.frat = Frat.objects.create(
                                        name="Alpha Epsilon Pi",
                                        chapter="Lambda",
                                        university="UChicago",
                                        password="password"
                                        )

        # Create a rush 
        self.rush1 = Rush.objects.create(
                                        first_name="Andrew", 
                                        last_name="Beinstein",
                                        phone_number="234234234",
                                        email="andrew@email.com",
                                        frat=self.frat
                                        )

        self.picture = Image.open("static/test.jpeg")

    def test_picture_upload_web(self):
        self.rush1.picture = self.picture
        self.rush1.save()

        self.assertTrue(self.rush1.picture_url)
        print self.rush1.picture_url

    def test_picture_upload_mobile(self):
        self.assertTrue(False)


