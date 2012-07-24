from django.views.generic import ListView

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from partidillos.partidillosapp.models import Match

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


class MatchesListViewHtml(ListView):

    context_object_name = "matches_list"
    template_name = 'partidillos/matches.html'
    extra_context = {}
    
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
        return self.request.user.get_profile().match_set.all()

class PendingMatchesListViewHtml(MatchesListViewHtml):

    extra_context= PendingContext().as_dict()

    def get_queryset(self):
        
        return Match.objects.exclude(players__id=self.request.user.id).filter(date__gt=datetime.now())
    
class MyMatchesListViewHtml(MatchesListViewHtml):

    extra_context= MyMatchesContext().as_dict()

    def get_queryset(self):
        
        return Match.objects.filter(creator__id=self.request.user.id).filter(date__gt=datetime.now())
    
