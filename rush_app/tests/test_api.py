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
        self.profile.frat.save()
        self.profile.save()

        # Create another user/userprofile
        self.user2 = User.objects.create_user('adam', "adam@email.com", 'adampassword')
        self.profile2 = UserProfile(user=self.user2, is_admin=True, frat=self.frat)
        self.profile2.save()

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

    def test_toggle_admin(self):
        url = '/api/v1/profile/{0}/toggle_admin/'.format(self.profile.pk)

        self.assertEqual(self.profile.is_admin, False)
        response = self.api_client.patch(url, data={})
        self.assertValidJSONResponse(response)

        self.profile = UserProfile.objects.get(pk=self.profile.pk)
        self.assertEqual(self.profile.is_admin, True)

        response = self.api_client.patch(url, data={})
        self.assertValidJSONResponse(response)
        self.profile = UserProfile.objects.get(pk=self.profile.pk)
        self.assertEqual(self.profile.is_admin, False)

    def test_create_profile_email(self):
        num_profiles = UserProfile.objects.count()
        data = {"email": "newprofile@email.com",
                "password": "newprofilepassword",
                "frat_name": self.frat.name,
                "frat_chapter": self.frat.chapter,
                "frat_password": "fratpassword",
                "is_admin": "False",
                "first_name": "New",
                "last_name": "Profile",
                }

        response = self.api_client.post('/api/v1/profile/create/', data=data)
        self.assertValidJSONResponse(response)
        self.assertEqual(UserProfile.objects.count(), num_profiles+1)

        # Check data returned is new profile
        response_data = self.deserialize(response)
        profile_response = self.api_client.get('/api/v1/profile/{0}/'.format(self.profile.pk))
        profile_data = self.deserialize(profile_response)
        self.assertKeys(response_data, profile_data)

        self.assertEqual(response_data['first_name'], "New")
        self.assertTrue(not response_data['is_admin'])

    def test_create_profile_facebook(self):
        num_profiles = UserProfile.objects.count()
        aepi = Frat.objects.create(name="Alpha Epsilon Pi", chapter="Lambda", password="immortal11")
        aepi.save()
        data = {
                    "is_admin": "True",
                    "first_name": "Adam",
                    "frat_name": "Alpha Epsilon Pi",
                    "password": "",
                    "last_name": "Gluck",
                    "frat_chapter": "Lambda",
                    "email": "",
                    "frat_password": "immortal11",
                    "facebook_id": "1247010773"
                }
        response = self.api_client.post('/api/v1/profile/create/', data=data)
        self.assertValidJSONResponse(response)
        self.assertEqual(UserProfile.objects.count(), num_profiles+1)

        # Check data returned is new profile
        response_data = self.deserialize(response)
        profile_response = self.api_client.get('/api/v1/profile/{0}/'.format(self.profile.pk))
        profile_data = self.deserialize(profile_response)
        self.assertKeys(response_data, profile_data)
        self.assertEqual(response_data["first_name"], data["first_name"])
        self.assertTrue(response_data['is_admin'])

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

    def test_thumbs_up(self):
        ''' Tests thumbs up functionality '''
        old_thumbsup = self.reputation.thumbsup
        old_thumbsup_users = self.reputation.thumbsup_users

        data = {"rush": self.rush.pk, 
                "user": self.profile2.pk}

        response = self.api_client.post('/api/v1/reputation/endorse/', data=data)
        self.reputation.save()

        self.assertValidJSONResponse(response)

        old_thumbsup_users.add(self.profile2)
        self.assertListEqual(list(self.reputation.thumbsup_users.all()), list(old_thumbsup_users.all()))
        self.assertEqual(self.reputation.thumbsup, old_thumbsup + 1)
        
        response = self.api_client.post('/api/v1/reputation/unendorse/', data=data)
        self.reputation.save()

        self.assertEqual(self.reputation.thumbsup, old_thumbsup)
        self.assertListEqual(list(self.reputation.thumbsup_users.all()), list(old_thumbsup_users.all()))

    # def test_picture(self):
        
    




        




                












