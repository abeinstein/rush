from django.conf.urls import patterns, url
from rush_app import views

from .views import thumbs, add_comment, home

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^rushes/$', views.all_frats, name="all_frats"),
    url(r'^rushes/(?P<frat_id>\d+)/$', views.show_frat, name="show_frat"), 
    # url(regex=r'^rushes/$', 
    #     view=RushListView.as_view(),
    #     name="rush_list"),
    url(r'^thumbs/(\d)/(\d)/(\d)/$', thumbs, name="thumbs"),
    url(r'^add_comment/(\d+)/(\d+)/$', add_comment, name="add_comment"),
)