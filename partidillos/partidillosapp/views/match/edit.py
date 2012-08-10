
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
    print "RequestPost:{0}".format(request.POST)
    if request.method == 'POST': # If the form has been submitted...
        mydict = request.POST.copy()
        mydict.update({'date':_get_date(request.POST['hora'],request.POST['dia'])})
        mydict.update({'creator': request.user.get_profile().pk})
        form = models.MatchForm(mydict,instance=instance)

        if form.is_valid(): # All validation rules pass
            form.save()
            return http.HttpResponseRedirect('/mymatches.html')
    else:
        form = models.MatchForm(instance=instance)

    return shortcuts.render(request, 'partidillos/creatematch.html', { 'form':
        form, 'pk': pk})


def _create_form(date, place, userid, invited, instance=None):
    """ Given the form data return the form for the Match model."""
    print "invited:{0}".format(invited)
    matchdict = { 'place': place , 'date': date, 'creator': userid,
            'invited': invited}
    return 

def _get_date(time, day):
    datetimestr = "{0} {1}".format(day, time)
    zone = timezone('Europe/Madrid')
    try:
        date = zone.localize(datetime.strptime(datetimestr, "%d-%m-%Y %H:%M"))
    except ValueError:
        date = None
    return date

@login_required
def update_match(request, pk, funcName):
    user = request.user.get_profile()
    func = globals()[funcName]
    return func(user, models.Match.objects.get(pk=pk))

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

def delete(user, match):
    if not user or not (user == match.creator):
        return http.HttpResponseForbidden()
    else:
        match.delete()
        return http.HttpResponseRedirect('/mymatches.html')
