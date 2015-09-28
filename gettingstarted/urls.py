from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout




import hello.views

urlpatterns = patterns('',

    url(r'^login/$',  login,  {'template_name' : 'login.html' }, name='login'),
    url(r'^logout/$',  logout, {'next_page': '/'}),
    url(r'^rules/?$', hello.views.rules, name='rules'),
    url(r'^results/?$', hello.views.week_results, name='results'),
    url(r'^team/?$', hello.views.team, name='team'),
    url(r'^bid/(?P<nfl_id>[0-9]+)/?$', hello.views.bid, name='bid'),
    url(r'^search/?$', hello.views.search, name='search'),
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),

)
