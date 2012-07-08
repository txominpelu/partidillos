from django.conf.urls import patterns, include, url
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListModelView, InstanceModelView
from partidillos.partidillosapp.models import Match
from partidillos.partidillosapp import views

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

class MatchesResource(ModelResource):
    fields = ['id', 'date', 'place', 'players'] 
    model = Match

class JoinedMatchesListView(ListModelView):

    def get(self, request, *args, **kwargs):
        return request.user.get_profile().match_set.all()

login_index = login_required(TemplateView.as_view(template_name='partidillos/matches.html'))

class PendingMatchesListView(ListModelView):

    def get(self, request, *args, **kwargs):
        return Match.objects.exclude(players__id=request.user.id)

urlpatterns = patterns('',
    url(r'^api/matches/(?P<matchId>\d{1,10})/(?P<funcName>join|leave)/$', views.updatePlayers),
    url(r'^api/matches/joined/$',
        JoinedMatchesListView.as_view(resource=MatchesResource)),
    url(r'^api/matches/pending/$',
        PendingMatchesListView.as_view(resource=MatchesResource)),
    # Examples:
    # url(r'^$', 'partidillos.views.home', name='home'),
    url(r'^index.html$', login_index),
    url(r'^create-match.html$', views.creatematch),

)
