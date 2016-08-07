from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

import json
from django.core import serializers
from main.utils import helper_util


def logs(request, logentry_id=None):
    if request.method == 'GET':
        # if logentry_id is None:
        #     return HttpResponse(status=403)

        # goal_entries = GoalEntry.objects.filter(goal=goal)
        # serialized_goal = serializers.serialize('json', [goal])
        # serialized_goal_entries = serializers.serialize('json', goal_entries)
        # return HttpResponse(json.dumps({
        #     'goal': serialized_goal,
        #     'goal_entries': serialized_goal_entries
        # }))
        return HttpResponse("GET LOGS", status=200)
    elif request.method == 'POST':
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)
