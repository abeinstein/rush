import json
from django.contrib.auth.models import User

from tastypie.test import ResourceTestCase

from rush_app.models import UserProfile, Frat, Rush, Reputation


class TastypieTest(ResourceTestCase):
    def setUp(self):
        super(TastypieTest, self).setUp()

        # Create a frat
        self.frat = Frat(name="Alpha Epsilon Test", 
                        chapter="Lambda", 
                        university="UChicago",
                        password="fratpassword")
        self.frat.save()

        # Create a user/userprofile
        self.user = User.objects.create_user('andrew', "andrew@email.com", 'profilepassword')
        self.profile = UserProfile(user=self.user, is_admin=False, frat=self.frat)
        self.profile.save()

        rush_info = {"first_name": "Brett",
                    "last_name": "Parket", 
                    "phone_number": "123456789",
                    "email": "brett@yahoo.com",
                    "notes": "Cool dude",
                    "frat": self.frat}

        self.rush = Rush(**rush_info)
        self.rush.save()

        self.reputation = Reputation.objects.create(rush=self.rush)
        self.reputation.thumbsup_users.add(self.profile)
        self.reputation.save()
    

    # Rush resource tests

    def test_get_detail_rush(self):
        response = self.api_client.get('/api/v1/rush/{0}/'.format(str(self.rush.pk)))
        self.assertValidJSONResponse(response)

    # Frat resource tests

    def test_get_detail_frat(self):
        response = self.api_client.get('/api/v1/frat/{0}/'.format(str(self.frat.pk)))
        self.assertValidJSONResponse(response)

    def test_create_frat(self):
        count = Frat.objects.count()
        data = {"name": "Phi Delta Theta",
                "chapter": "Douchy",
                "university": "UChicago",
                "password": "phideltpassword"}
        response = self.api_client.post('/api/v1/frat/create/', data=data)
        self.assertHttpCreated(response)
        self.assertEqual(Frat.objects.count(), count+1)

    # UserProfile resource tests

    def test_get_detail_profile(self):
        response = self.api_client.get('/api/v1/profile/{0}/'.format(str(self.profile.pk)))
        self.assertValidJSONResponse(response)

    def test_create_profile_email(self):
        num_profiles = UserProfile.objects.count()
        data = {"email": "newprofile@email.com",
                "password": "newprofilepassword",
                "frat_name": self.frat.name,
                "frat_chapter": self.frat.chapter,
                "frat_password": "fratpassword"}

        response = self.api_client.post('/api/v1/profile/create/', data=data)
        self.assertValidJSONResponse(response)
        self.assertEqual(UserProfile.objects.count(), num_profiles+1)

        # Check data returned is new profile
        response_data = self.deserialize(response)
        profile_response = self.api_client.get('/api/v1/profile/{0}/'.format(self.profile.pk))
        profile_data = self.deserialize(profile_response)
        self.assertKeys(response_data, profile_data)

    def test_create_profile_facebook(self):
        num_profiles = UserProfile.objects.count()
        data = {"facebook_id": "23492912",
                "frat_name": self.frat.name,
                "frat_chapter": self.frat.chapter,
                "frat_password": "fratpassword"}
        response = self.api_client.post('/api/v1/profile/create/', data=data)
        self.assertValidJSONResponse(response)
        self.assertEqual(UserProfile.objects.count(), num_profiles+1)

        # Check data returned is new profile
        response_data = self.deserialize(response)
        profile_response = self.api_client.get('/api/v1/profile/{0}/'.format(self.profile.pk))
        profile_data = self.deserialize(profile_response)
        self.assertKeys(response_data, profile_data)

    def test_create_profile_invalid_frat(self):
        data = {"email": "some@email.com",
                "password": "somepassword",
                "frat_name": "Iota Don't Exist",
                "frat_chapter": "Omicron",
                "frat_password": "password"}
        response = self.api_client.post('/api/v1/profile/create/', data=data)
        self.assertHttpBadRequest(response)

    def test_create_profile_invalid_frat_password(self):
        data = {"email": "newprofile@email.com",
                "password": "newprofilepassword",
                "frat_name": self.frat.name,
                "frat_chapter": self.frat.chapter,
                "frat_password": "invalidfratpassword"}
        response = self.api_client.post('/api/v1/profile/create/', data=data)
        self.assertHttpBadRequest(response)

    def test_create_profile_user_already_exists(self):
        data = {"email": self.user.email,
                "password": "profilepassword",
                "frat_name": self.frat.name,
                "frat_chapter": self.frat.chapter,
                "frat_password": "invalidfratpassword"}
        response = self.api_client.post('/api/v1/profile/create/', data=data)
        self.assertHttpBadRequest(response)

    # Reputation resource tests
    def test_get_list_reputation(self):
        ''' Tests GET /api/v1/reputation/ '''
        response = self.api_client.get('/api/v1/reputation/')
        self.assertValidJSONResponse(response)
        



        




                












