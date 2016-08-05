from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

import json
from django.core import serializers
from main.utils import helper_util

###############################################
############### HELPER METHODS ################
###############################################


def get_goal(goal_id):
    if goal_id is None return None
    try:
        goal = Goal.objects.get(id=goal_id)
        return goal
    except Goal.DoesNotExist:
        return None

#################################################
############# REST API ENDPOINT #################
#################################################


def goals(request, goal_id=None):
    goal = get_goal(goal_id)

    # Get list of all goals
    if request.method == 'GET':
        if goal is None:
            return HttpResponse(status=403)

        goal_entries = GoalEntry.objects.filter(goal=goal)
        serialized_goal = serializers.serialize('json', [goal])
        serialized_goal_entries = serializers.serialize('json', goal_entries)
        return HttpResponse(json.dumps({
            'goal': serialized_goal,
            'goal_entries': serialized_goal_entries
        }))

    # Delete goal
    elif request.method == 'DELETE':
        if goal is None:
            return HttpResponse(status=403)

        goal.delete()
        return HttpResponse(status=200)

    elif request.method == 'POST':
        fbid = request.POST['fbid']
        if helper_util.user_exists(fbid):
            current_user = User.objects.get(fbid=fbid)
        else:
            return HttpResponse(status=200)

        name = request.POST['name']
        send_text = request.POST['send_text']
        send_time_utc = request.POST['send_time_utc']
        response_type = request.POST['response_type']

        goal = Goal(
            user=current_user,
            name=name,
            send_text=send_text,
            send_time_utc=send_time_utc,
            response_type=response_type
        )
        goal.save()

        return HttpResponse(status=200)
    # Error 404 Not Found
    else:
        return HttpResponse(status=403)

############################################
################# VIEWS ####################
############################################


# List all goals for a given user
def list(request, fbid):
    if not helper_util.user_exists(fbid):
        return HttpResponse(status=404)

    current_user = User.objects.get(fbid=fbid)
    if(not current_user):
        return HttpResponse("Invalid user")

    goals_list = Goal.objects.filter(user=current_user)
    serialized_response = serializers.serialize('json', goals_list)

    context = RequestContext(request, {
        'fbid': fbid,
        'goals': goals_list
    })
    template = loader.get_template('goals/list.html')
    return HttpResponse(template.render(context))


# Allow users to see entries for a given goal
def show(request, goal_id):
    if not goal_exists(goal_id):
        return HttpResponse(status=404)

    goal = Goal.objects.get(id=goal_id)
    goal_entries = GoalEntry.objects.filter(goal=goal)

    context = RequestContext(request, {
        'goal': goal,
        'goal_entries': goal_entries
    })
    template = loader.get_template('goals/show.html')
    return HttpResponse(template.render(context))


# Allow users to add a goal
def add_goal_page(request, fbid):
    if not helper_util.user_exists(fbid):
        return HttpResponse(status=404)

    current_user = User.objects.get(fbid=fbid)
    if(not current_user):
        return HttpResponse("Invalid user")

    context = RequestContext(request, {
        'fbid': fbid
    })
    template = loader.get_template('goals/add.html')
    return HttpResponse(template.render(context))
