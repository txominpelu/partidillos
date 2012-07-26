from django.conf.urls import patterns, include, url

from partidillos.partidillosapp.models import Match
from partidillos.partidillosapp.views import matches
from partidillos.partidillosapp.views import main

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from django.views.generic.detail import DetailView


class MatchDetailView(DetailView):

    model = Match
    template_name='partidillos/match.html'
    # Defines the context name in the template
    context_object_name = 'match'
    

urlpatterns = patterns('',
    # url(r'^$', 'partidillos.views.home', name='home'),
    url(r'^$', matches.JoinedMatchesListViewHtml.as_view() ),
    url(r'^joined.html$', matches.JoinedMatchesListViewHtml.as_view() ),
    url(r'^pending.html$', matches.PendingMatchesListViewHtml.as_view() ),
    url(r'^mymatches.html$', matches.MyMatchesListViewHtml.as_view() ),
    url(r'^match/(?P<pk>[\d]+)/$', MatchDetailView.as_view()),
    url(r'^match/create/$', main.creatematch),
    url(r'^match/(?P<pk>[\d]+)/edit/$', main.creatematch),
    url(r'^match/(?P<pk>\d{1,10})/(?P<funcName>join|leave|delete)/$',
        main.update_match),
    # Examples:

)
