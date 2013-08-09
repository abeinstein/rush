from django.conf.urls import patterns, include, url
from django.contrib import admin
from rush_app.views import all_frats, show_frat
from django.contrib.auth.views import login, logout

admin.autodiscover()

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
)
