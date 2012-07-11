from django.conf.urls import patterns, include, url
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListModelView, InstanceModelView
from partidillos.partidillosapp.models import Match
from partidillos.partidillosapp import views

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from datetime import datetime

class MatchesResource(ModelResource):
    fields = ['id', 'date', 'place', 'players'] 
    model = Match

class MatchesListViewHtml(ListView):

    context_object_name = "matches_list"
    template_name = 'partidillos/matches.html'
    extra_context = {}
    
    def get(self, request, *args, **kwargs):
        return super(MatchesListViewHtml, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MatchesListViewHtml, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context

class JoinedMatchesListViewHtml(MatchesListViewHtml):

    extra_context={'title':'Voy a jugar', 'action': 'leave',
                  'oppositepage': 'pending',
                  'oppositetitle': 'Partidos disponibles'}

    def get_queryset(self):
        return self.request.user.get_profile().match_set.all()

class PendingMatchesListViewHtml(MatchesListViewHtml):

    extra_context={'title':'Partidos disponibles', 'action': 'join',
                  'oppositepage': 'joined',
                  'oppositetitle': 'Voy a jugar'}

    def get_queryset(self):
        
        return Match.objects.exclude(players__id=self.request.user.id).filter(date__gt=datetime.now())
    

login_joined = login_required( JoinedMatchesListViewHtml.as_view())
login_pending = login_required( PendingMatchesListViewHtml.as_view())


urlpatterns = patterns('',
    url(r'^api/matches/(?P<matchId>\d{1,10})/(?P<funcName>join|leave)/$', views.updatePlayers),
    # Examples:
    # url(r'^$', 'partidillos.views.home', name='home'),
    url(r'^joined.html$', login_joined ),
    url(r'^pending.html$', login_pending ),
    url(r'^create-match.html$', views.creatematch),

)
