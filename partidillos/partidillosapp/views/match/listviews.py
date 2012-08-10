from django.views.generic import ListView

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from partidillos.partidillosapp.models import Match
from django.utils import timezone

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
    onclick = 'edit/'
    links = ['JoinedContext', 'PendingContext'] 


class MatchesListViewHtml(ListView):

    context_object_name = "matches_list"
    template_name = 'partidillos/matches.html'
    extra_context = {}
    
    def filter_outdated(self, queryset): 
        print "timezone: {0}".format(timezone.now())
        return queryset.filter(date__gt=timezone.now())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MatchesListViewHtml, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(MatchesListViewHtml, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MatchesListViewHtml, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class JoinedMatchesListViewHtml(MatchesListViewHtml):

    extra_context= JoinedContext().as_dict()

    def get_queryset(self):
        return self.filter_outdated(self.request.user.get_profile().match_set)

class PendingMatchesListViewHtml(MatchesListViewHtml):

    extra_context= PendingContext().as_dict()

    def get_queryset(self):
        
        return self.filter_outdated(Match.objects.exclude(players__id=self.request.user.id).filter(invited__id=self.request.user.id))
    
class MyMatchesListViewHtml(MatchesListViewHtml):

    extra_context= MyMatchesContext().as_dict()

    def get_queryset(self):
        return self.get_mymatches(self.request.user)
        

    def get_mymatches(self, user):
        return self.filter_outdated(Match.objects.filter(creator__id=user.id))
    
