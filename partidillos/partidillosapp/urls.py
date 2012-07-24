from django.conf.urls import patterns, include, url
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListModelView, InstanceModelView
from partidillos.partidillosapp.models import Match
from partidillos.partidillosapp import views

from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from django.views.generic.detail import DetailView

from datetime import datetime

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

class Context(object):

    def as_dict(self):
        self.links = [ globals()[link]() for link in self.links]
        return [(name, getattr(self,name)) for name in dir(self) 
                if not callable(getattr(self,name)) and 
                not name.startswith('__')]

class JoinedContext(Context):

    title = 'Voy a jugar'
    action = 'leave'
    icon = 'star'
    page = 'joined'
    links = ['PendingContext', 'MyMatchesContext'] 

class PendingContext(Context):

    title = 'Disponibles'
    action = 'join'
    icon = 'arrow-l'
    page = 'pending'
    links = ['JoinedContext', 'MyMatchesContext'] 

class MyMatchesContext(Context):

    title = 'Mis partidos'
    page = 'mymatches'
    links = ['JoinedContext', 'PendingContext'] 

class JoinedMatchesListViewHtml(MatchesListViewHtml):

    extra_context= JoinedContext().as_dict()

    def get_queryset(self):
        return self.request.user.get_profile().match_set.all()

class PendingMatchesListViewHtml(MatchesListViewHtml):

    extra_context= PendingContext().as_dict()

    def get_queryset(self):
        
        return Match.objects.exclude(players__id=self.request.user.id).filter(date__gt=datetime.now())
    
class MyMatchesListViewHtml(MatchesListViewHtml):

    extra_context= MyMatchesContext().as_dict()

    def get_queryset(self):
        
        return Match.objects.filter(creator__id=self.request.user.id).filter(date__gt=datetime.now())
    

class MatchDetailView(DetailView):

    model = Match
    template_name='partidillos/match.html'
    # Defines the context name in the template
    context_object_name = 'match'
    
login_joined = login_required( JoinedMatchesListViewHtml.as_view())
login_pending = login_required( PendingMatchesListViewHtml.as_view())
login_mymatches = login_required( MyMatchesListViewHtml.as_view())

urlpatterns = patterns('',
    url(r'^api/matches/(?P<matchId>\d{1,10})/(?P<funcName>join|leave)/$', views.updatePlayers),
    # Examples:
    # url(r'^$', 'partidillos.views.home', name='home'),
    url(r'^$', login_joined ),
    url(r'^joined.html$', login_joined ),
    url(r'^pending.html$', login_pending ),
    url(r'^mymatches.html$', login_mymatches ),
    url(r'^match/(?P<pk>[\d]+)/$', MatchDetailView.as_view()),
    url(r'^create-match.html$', views.creatematch),

)
