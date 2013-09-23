from django.conf.urls import patterns, url
from rush_app import views

from .views import thumbs, add_comment, home, RushCreateView, RushUpdateView, RushDeleteView

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^rushes/$', views.all_frats, name="all_frats"),
    url(r'^rushes/(?P<frat_id>\d+)/$', views.show_frat, name="show_frat"), 
    url(r'^rushes/add/$', RushCreateView.as_view(), name="add_rush"),
    url(r'^rushes/edit/(?P<pk>\d+)/$', RushUpdateView.as_view(), name="edit_rush"),
    url(r'^rushes/delete/(?P<pk>\d+)/$', RushDeleteView.as_view(), name="delete_rush"),

    url(r'^thumbs/(\d)/(\d+)/(\d+)/$', thumbs, name="thumbs"),
    url(r'^add_comment/(\d+)/(\d+)/$', add_comment, name="add_comment"),
)