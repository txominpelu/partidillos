from django.conf.urls import patterns, include, url

from partidillos.partidillosapp.models import Match
from partidillos.partidillosapp.views.match import listviews
from partidillos.partidillosapp.views.match import edit

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
    url(r'^$', listviews.JoinedMatchesListViewHtml.as_view() ),
    url(r'^joined.html$', listviews.JoinedMatchesListViewHtml.as_view() ),
    url(r'^pending.html$', listviews.PendingMatchesListViewHtml.as_view() ),
    url(r'^mymatches.html$', listviews.MyMatchesListViewHtml.as_view() ),
    url(r'^match/(?P<pk>[\d]+)/$', MatchDetailView.as_view()),
    url(r'^match/create/$', edit.creatematch),
    url(r'^match/(?P<pk>[\d]+)/edit/$', edit.creatematch),
    url(r'^match/(?P<pk>\d{1,10})/(?P<funcName>join|leave|delete)/$',
        edit.update_match),
    # Examples:

)
