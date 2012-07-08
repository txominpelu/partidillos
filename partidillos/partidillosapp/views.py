
from django import shortcuts
from django.template import RequestContext

from partidillos.partidillosapp import models

from django import http
from django.core import serializers

from django.contrib.auth.decorators import login_required

from datetime import datetime

@login_required
def creatematch(request):
    if request.method == 'POST': # If the form has been submitted...
        form = _create_creatematchform(request.POST['hora'],
                request.POST['dia'],request.POST['place'])
        if form.is_valid(): # All validation rules pass
            form.save()
            return http.HttpResponseRedirect('/partidillos/index.html')
    else: 
        print "Tal"
        form = models.MatchForm()

    return shortcuts.render(request, 'partidillos/creatematch.html', { 'form': form, })

def _create_creatematchform(time, day, place):
    """ Given the form data return the form for the Match model."""
    datetimestr = "{0} {1}".format(day, time)
    try:
        date = datetime.strptime(datetimestr, "%Y-%m-%d %H:%M")
    except ValueError:
        date = None
    matchdict = { 'place': place , 'date': date}
    return models.MatchForm(matchdict)

@login_required
def updatePlayers(request, matchId, funcName):
    user = request.user.get_profile()
    func = globals()[funcName]
    return func(user, models.Match.objects.get(pk=matchId))

def join(user, match):
    if not user or user in match.players.all() :
        return http.HttpResponseForbidden()
    else:
        match.players.add(user)
        match.save()
        return http.HttpResponse("success", mimetype='application/javascript')

def leave(user, match):
    if not user or user not in match.players.all():
        return http.HttpResponseForbidden()
    else:
        match.players.remove(user)
        match.save()
        return http.HttpResponse("success", mimetype='application/javascript')
