from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *

import json
from django.core import serializers

# Helper method
def user_exists(fbid):
    try:
        user = User.objects.get(fbid=fbid)
        return True
    except User.DoesNotExist:
        return False

def goal_exists(goal_id):
    try:
        goal = Goal.objects.get(id=goal_id)
        return True
    except Goal.DoesNotExist:
        return False

# REST endpoint
def goals(request, fbid):
    print('GOALS REST ENDPOINT')
    if not user_exists(fbid):
        print("User doesn't exist")
        return HttpResponse(status=404)

    print("User exists!")
    current_user = User.objects.get(fbid=fbid)
        
    # Get list of all goals
    if request.method == 'GET':
        goals_list = Goal.objects.filter(user=current_user)
        serialized_response = serializers.serialize('json', goals_list)
        return HttpResponse(serialized_response)

    # Create new goal
    elif request.method == 'POST':
        current_user = User.objects.get(fbid=fbid)

        name = request.POST['name']
        send_text = request.POST['send_text']
        send_time_utc = request.POST['send_time_utc']
        response_type = request.POST['response_type']

        g = Goal(user=current_user, name=name, send_text=send_text, send_time_utc=send_time_utc, response_type=response_type)
        g.save()

        return HttpResponse(status=200)

    # Delete goal
    elif request.method == 'DELETE':
        return HttpResponse(status=200)
    # Error 404 Not Found
    else:
        return HttpResponse(status=404)

# Views

# List all goals for a given user
def list(request, fbid):
    if not user_exists(fbid):
        return HttpResponse(status=404)

    current_user = User.objects.get(fbid=fbid)
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
def add(request, fbid):
    if not user_exists(fbid):
        return HttpResponse(status=404)
        
    context = RequestContext(request, {
        'fbid': fbid
    })
    template = loader.get_template('goals/add.html')
    return HttpResponse(template.render(context))

