from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change
import hello.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$',  login,  {'template_name' : 'login.html' }, name='login'),
    url(r'^password/$',  password_change, {'post_change_redirect': '/team', 
                                           'template_name': 'password_change_form.html'}, 
                                           name='password_change'),
    url(r'^logout/$',  logout, {'next_page': '/'}),
    url(r'^rules/?$', hello.views.rules, name='rules'),
    url(r'^results/(?P<week>[0-9]+)?/?$', hello.views.week_results, name='results'),
    url(r'^team/(?P<team_id>[0-9]+)?/?$', hello.views.team, name='team'),
    url(r'^bid/(?P<nfl_id>[0-9]+)/?$', hello.views.bid, name='bid'),
    url(r'^biddelete/(?P<bid_id>.*)/?$', hello.views.delete_bid, name='delete_bid'),
    url(r'^process_on_nfl/(?P<bid_id>.*)/?$', hello.views.process_on_nfl, name='process_bid'),
    url(r'^search/?$', hello.views.search, name='search'),
    url(r'^$', hello.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
