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

def index(request, fbid):
    # Get user
    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)

    # Get log for this user
    user_log = Log.find_or_create(current_user)

    log_context_list = LogContext.objects.filter(log=user_log)
    
    context = RequestContext(request, {
        'fbid': fbid,
        'log_context_list' : log_context_list
    })
    template = loader.get_template('log/index.html')
    return HttpResponse(template.render(context))

def log_context(request, fbid, log_context_id):
    # Get objects
    log_context = LogContext.objects.get(log_context_id)

    context = RequestContext(request, {
        'fbid': fbid,
        'log_context' : log_context
    })
    template = loader.get_template('log/log_context.html')
    return HttpResponse(template.render(context))


