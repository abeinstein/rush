from django.conf.urls import patterns, include, url
from django.contrib import admin
from rush_app.views import all_frats, show_frat
from django.contrib.auth.views import login, logout
from tastypie.api import Api
from rush_app.api.resources import RushResource

admin.autodiscover()
v1_api = Api(api_name='v1')
v1_api.register(RushResource())

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('rush_app.urls')),
    # url(r'^rush/', include('rush.foo.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login, name="login"),
    url(r'^logout/', logout, {'next_page': '/'}, name="logout"),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^api/', include(v1_api.urls)),
)
