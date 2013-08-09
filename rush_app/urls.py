from django.conf.urls import patterns, url
from rush_app import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^rushes/$', views.all_frats, name="all_frats"),
    url(r'^rushes/(?P<frat_id>\d+)/$', views.show_frat, name="show_frat"), 
    url(r'^thumbs/(\d)/(\d)/(\d)/$', views.thumbs, name="thumbs")



)