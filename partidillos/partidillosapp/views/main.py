
from django import shortcuts
from django.template import RequestContext

from partidillos.partidillosapp import models

from django import http
from django.core import serializers

from django.contrib.auth.decorators import login_required

from datetime import datetime
from pytz import timezone
from django.utils.timezone import utc

@login_required
def creatematch(request, pk=None):
    instance = models.Match.objects.get(pk=pk) if pk else None
    # TODO: only creator
    # Check that if it's a post and is editing an existing match
    # the user making the request has to be the creator
    if request.method == 'POST': # If the form has been submitted...
        form = _create_form(_get_date(request.POST['hora'],request.POST['dia']),
                request.POST['place'], request.user.get_profile().pk, instance)

        if form.is_valid(): # All validation rules pass
            form.save()
            return http.HttpResponseRedirect('/mymatches.html')
    else:
        form = models.MatchForm(instance=instance)

    return shortcuts.render(request, 'partidillos/creatematch.html', { 'form': form, })



def _create_form(date, place, userid, instance=None):
    """ Given the form data return the form for the Match model."""
    matchdict = { 'place': place , 'date': date, 'creator': userid}
    return models.MatchForm(matchdict,instance=instance)

def _get_date(time, day):
    datetimestr = "{0} {1}".format(day, time)
    zone = timezone('Europe/Madrid')
    try:
        date = zone.localize(datetime.strptime(datetimestr, "%Y-%m-%d %H:%M"))
    except ValueError:
        date = None
    return date

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
        return http.HttpResponseRedirect('/joined.html')

def leave(user, match):
    if not user or user not in match.players.all():
        return http.HttpResponseForbidden()
    else:
        match.players.remove(user)
        match.save()
        return http.HttpResponseRedirect('/joined.html')
