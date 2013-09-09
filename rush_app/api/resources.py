from tastypie import fields
from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpCreated, HttpAccepted, HttpBadRequest, HttpGone
from tastypie.authorization import Authorization, DjangoAuthorization, Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from rush_app.config import Codes
from rush_app.models import Rush, Frat, UserProfile, Comment, Reputation

RESOURCE_ROOT = 'rush_app.api.resources'

# TODO: FUCKING CHANGE THE AUTHORIZATION!!!

class FratResource(ModelResource):
    rushes = fields.ToManyField("%s.RushResource" % RESOURCE_ROOT, 'rush_set', full=True, related_name='frat')
    members = fields.ToManyField("%s.UserProfileResource" % RESOURCE_ROOT, 
                                'userprofile_set', full=True, related_name='frat')


    class Meta:
        queryset = Frat.objects.all()
        allowed_methods = ['get', 'post', 'patch', 'delete']
        authorization = Authorization()
        filtering = {
            'name': ALL,
            'chapter': ALL,
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/create/$" % 
                self._meta.resource_name, self.wrap_view('create'), 
                name="api_create_frat")
        ]

    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body) 
        name = data.get('name', '')
        chapter = data.get('chapter', '')
        university = data.get('university', '')
        password = data.get('password', '')

        try:
            frat = Frat(name=name, chapter=chapter, university=university, password=password)
            frat.save()
            return self.create_response(request, {'id': frat.pk}, response_class=HttpCreated)
        except:
            error_message = "Frat could not be created"
            return self.create_response(request, {'message': error_message}, 
                                        response_class=HttpBadRequest)


class RushResource(ModelResource):
    frat = fields.ForeignKey(FratResource, 'frat')
    #comments = fields.ToManyField('rush_app.api.resources.CommentResource', 'comment_set', related_name='rush', full=True)

    class Meta:
        queryset = Rush.objects.all()
        allowed_methods = ['get', 'post', 'patch', 'delete']
        authorization = Authorization()

class UserProfileResource(ModelResource):
    user = fields.ToOneField("%s.UserResource" % RESOURCE_ROOT, 'user', full=True)
    frat = fields.ForeignKey(FratResource, 'frat')

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = "profile"
        allowed_methods = ['get', 'post', 'patch']
        authorization = Authorization()
        always_return_data = True
        #authentication = BasicAuthentication() 

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
            url(r"^(?P<resource_name>%s)/(?P<facebook_id>\w+)/fb/$" % 
                self._meta.resource_name, self.wrap_view('dispatch_detail'), 
                name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/sign_in/$" %
                self._meta.resource_name,
                self.wrap_view('sign_in'), name="api_sign_in"),
            url(r"^(?P<resource_name>%s)/create/$" %
                self._meta.resource_name,
                self.wrap_view('create'), name="api_create"),
        ]

    def sign_in(self, request, **kwargs):
        ''' Verifies that a user is in the database '''
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body) 
        username = data.get('email', '')
        password = data.get('password', '')
        facebook_id = data.get('facebook_id', '')
        user = authenticate(username=username, password=password)

        if user:
            return self.create_response(request, {'is_verified': 1, 'id': user.id})
        else:
            try:
                profile = UserProfile.objects.get(facebook_id=facebook_id)
                return self.create_response(request, {'is_verified': 1, 'id': profile.user.id})
            except ObjectDoesNotExist:
                return self.create_response(request, {'is_verified': 0})
                

    # def obj_create(self, bundle, **kwargs):
    #     email = bundle.data.get('email', '')
    #     password = bundle.data.get('password', '')
    #     facebook_id = bundle.data.get('facebook_id', '')
    #     frat_name = bundle.data.get('frat_name', '')
    #     frat_chapter = bundle.data.get('frat_chapter', '')
    #     frat_password = bundle.data.get('frat_password', '')


    #     return super(UserProfileResource).obj_create(bundle, **kwargs)

    # TODO: Hook into native POST
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
            error_message = "Frat cannot be found!"
            return self.create_response(request, {"message": error_message},
                                        response_class=HttpBadRequest
                                        )

        hashed_password = frat.password
        if check_password(frat_password, hashed_password):
            # Frat exists, will create user
            if facebook_id:
                try:
                    u = User.objects.create_user(facebook_id)
                except IntegrityError:
                    error_message = "User already exists"
                    return self.create_response(request, {"message": error_message, "duplicate": 1},
                                            response_class=HttpBadRequest)
            elif email and password:
                # Note: we are using email as the username
                try:
                    u = User.objects.create_user(email, email, password)
                except IntegrityError:
                    error_message = "User already exists"
                    return self.create_response(request, {"message": error_message, "duplicate": 1},
                                            response_class=HttpBadRequest)
            else:
                error_message = "Please provide either email/password or facebook id"
                return self.create_response(request, 
                                            {"message": error_message},
                                            response_class=HttpBadRequest
                                            )

            u.save()


            # Now, will create user profile
            pro = UserProfile(user=u, frat=frat)
            if facebook_id:
                pro.facebook_id = facebook_id
            pro.save()

            return self.get_detail(request, pk=pro.pk)
        else:
            error_message = "Frat found, but invalid password"
            return self.create_response(request, 
                                        {"message": error_message},
                                        response_class=HttpBadRequest)



class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()


class CommentResource(ModelResource):
    rush = fields.ToOneField(RushResource, 'rush')
    profile = fields.ToOneField(UserProfileResource, 'userprofile', full=True)

    class Meta:
        queryset = Comment.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        authorization = Authorization() 
        filtering = {
            'rush': ALL_WITH_RELATIONS,
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add/$" %
                self._meta.resource_name,
                self.wrap_view('add'), name="api_add_comment"),
        ]

    # TODO: Hook this onto native POST request
    def add(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body)

        rush_id = data.get('rush_id', '')
        prof_id = data.get('prof_id', '')
        body = data.get('body', '')

        if not rush_id or not prof_id:
            error_message = "Please provide a non-blank rush_id and prof_id"
            return self.create_response(request, {'message': error_message}, 
                                        response_class=HttpBadRequest)

        try:
            rush = Rush.objects.get(pk=rush_id)
        except ObjectDoesNotExist:
            error_message = "Rush does not exist."
            return self.create_response(request, {'message': error_message},
                                        response_class=HttpBadRequest)

        try:
            prof = UserProfile.objects.get(pk=prof_id)
        except ObjectDoesNotExist:
            error_message = "Profile does not exist."
            return self.create_response(request, {'message': error_message},
                                        response_class=HttpBadRequest)

        comment = Comment(body=body, rush=rush, userprofile=prof)
        comment.save()
        return self.create_response(request, {}, response_class=HttpCreated)


class ReputationResource(ModelResource):
    rush = fields.ToOneField(RushResource, 'rush')
    thumbsup_users = fields.ToManyField(UserProfileResource, 'thumbsup_users')
    thumbsdown_users = fields.ToManyField(UserProfileResource, 'thumbsdown_users')

    class Meta:
        queryset = Reputation.objects.all()
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        filtering = {
            'rush': ALL_WITH_RELATIONS,
            'thumbsup_users': ALL_WITH_RELATIONS,
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/endorse/$" % 
                self._meta.resource_name, self.wrap_view('endorse'), 
                name="api_endorse"),
            url(r"^(?P<resource_name>%s)/unendorse/$" % 
                self._meta.resource_name, self.wrap_view('unendorse'), 
                name="api_unendorse")
        ]

    # TODO: DRY violation. Figure out how to use view
    def endorse(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body) 
        rush_id = data.get('rush', '')
        profile_id = data.get('user', '')

        if not (rush_id and profile_id):
            msg = "Please provide 'rush' field and 'user' field."
            return self.create_response(request, {'message': msg}, response_class=HttpBadRequest)

        try:
            rush = Rush.objects.get(pk=int(rush_id))
            profile = UserProfile.objects.get(pk=int(profile_id))
            reputation = rush.reputation
        except ObjectDoesNotExist:
            msg = "Rush or User does not exist"
            return self.create_response(request, {'message': msg}, response_class=HttpBadRequest)

        reputation.thumbsup_users.add(profile)
        reputation.save()
        rush.save()

        return self.create_response(request, {'message': 'Success'})

    def unendorse(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body) 
        rush_id = data.get('rush', '')
        profile_id = data.get('user', '')

        if not (rush_id and profile_id):
            msg = "Please provide 'rush' field and 'user' field."
            return self.create_response(request, {'message': msg}, response_class=HttpBadRequest)

        try:
            rush = Rush.objects.get(pk=int(rush_id))
            profile = UserProfile.objects.get(pk=int(profile_id))
        except ObjectDoesNotExist:
            msg = "Rush or User does not exist"
            return self.create_response(request, {'message': msg}, response_class=HttpBadRequest)

        rush.reputation.thumbsup_users.remove(profile)
        rush.reputation.save()

        return self.create_response(request, {'message': 'Success'})







