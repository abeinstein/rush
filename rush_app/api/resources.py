from tastypie import fields
from tastypie.resources import ModelResource
from rush_app.models import Rush, Frat, UserProfile
from django.contrib.comments import Comment
from django.contrib.auth.models import User
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.authentication import BasicAuthentication
from rush_app.config import Codes

RESOURCE_ROOT = 'rush_app.api.resources'


class FratResource(ModelResource):
    rushes = fields.ToManyField("%s.RushResource" % RESOURCE_ROOT, 'rush_set', full=True)
    members = fields.ToManyField("%s.UserProfileResource" % RESOURCE_ROOT, 
                                'userprofile_set', full=True)


    class Meta:
        queryset = Frat.objects.all()
        allowed_methods = ['get']


class RushResource(ModelResource):
    frat = fields.ForeignKey(FratResource, 'frat')
    comments = fields.ToManyField('rush_app.api.resources.CommentResource', 'comments', related_name='rush', full=True)

    class Meta:
        queryset = Rush.objects.all()
        allowed_methods = ['get']

class UserProfileResource(ModelResource):
    user = fields.ToOneField("%s.UserResource" % RESOURCE_ROOT, 'user', full=True)
    frat = fields.ForeignKey(FratResource, 'frat')

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = "profile"
        authentication = BasicAuthentication() # CHANGE!!

    def dehydrate(self, bundle):
        '''Merge userprofile with user field'''
        for key in bundle.data['user'].data.keys():
            try:
                bundle.data[key] = bundle.data['user'].obj.__getattribute__(key)
            except AttributeError:
                pass
        del bundle.data['user']
        return bundle


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s_fb)/(?P<facebook_id>\w+)/$" % 
                self._meta.resource_name, self.wrap_view('dispatch_detail'), 
                name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/login/$" %
                self._meta.resource_name,
                self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/create/$" %
                self._meta.resource_name,
                self.wrap_view('create'), name="api_create"),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body) 
        username = data.get('username', '')
        password = data.get('password', '')
        facebook_id = data.get('facebook_id', '')
        user = authenticate(username=username, password=password)
        if user:
            return self.create_response(request, {'success': Codes.LOGIN_SUCCESS})
        else:
            try:
                user = UserProfile.objects.get(facebook_id=facebook_id)
            except ObjectDoesNotExist:
                return self.create_response(request, {'success': Codes.LOGIN_FAILURE})
            else:
                return self.create_response(request, {'success': Codes.LOGIN_SUCCESS})

    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)

        email = data.get('email', '')
        password = data.get('password', '')
        facebook_id = data.get('facebook_id', '')
        frat_name = data.get('frat_name', '')
        frat_chapter = data.get('frat_chapter', '')
        frat_password = data.get('frat_password', '')

        # Check if the frat exists
        try:
            frat = Frat.objects.get(name=frat_name, chapter=frat_chapter)
        except ObjectDoesNotExist:
            response = Codes.FRAT_DOES_NOT_EXIST
        else:
            hashed_password = frat.password

            if check_password(frat_password, hashed_password):
                # Frat exists, will create user
                if facebook_id:
                    u = User.objects.create_user(facebook_id)
                elif email and password:
                    # Note: we are using email as the username
                    u = User.objects.create_user(email, email, password)
                else:
                    response = Codes.BLANK_REQUEST

                u.save()

                # Now, will create user profile
                pro = UserProfile(user=u, frat=frat)
                if facebook_id:
                    pro.facebook_id = facebook_id
                pro.save()

                response = Codes.USER_CREATED_SUCCESSFULLY
            else:
                response = Codes.FRAT_INVALID_PASSWORD

        return self.create_response(request, {'success': response})







class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()


class CommentResource(ModelResource):
    rush = fields.ToOneField(RushResource, 'content_object')
    user = fields.ToOneField(UserResource, 'user')

    class Meta:
        queryset = Comment.objects.all()



