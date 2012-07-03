
from django.shortcuts import render_to_response
from django.template import RequestContext

from partidillos.partidillosapp import models

from django import http
from django.core import serializers

from django.contrib.auth.decorators import login_required

@login_required
def partidillos(request):
    return render_to_response('partidillos/matches.html', {}, context_instance=RequestContext(request) ) 


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
