from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *
from main.entrypoints.messenger import send_api_helper
import json
from django.core import serializers
from main.utils import helper_util
from main.message_log import message_log
from django.views.decorators.csrf import csrf_exempt

###############################################
############### HELPER METHODS ################
###############################################

def get_habit(habit_id):
    if habit_id is None:
        return None
    try:
        habit = Habit.objects.get(id=habit_id)
        return habit
    except Habit.DoesNotExist:
        return None

#################################################
############# REST API ENDPOINT #################
#################################################
@csrf_exempt
def habits(request, habit_id=None):
    habit = get_habit(habit_id)

    # Get list of all habits
    if request.method == 'GET':
        if habit is None:
            return HttpResponse(status=403)

        habit_entries = HabitEntry.objects.filter(habit=habit)
        serialized_habit = serializers.serialize('json', [habit])
        serialized_habit_entries = serializers.serialize('json', habit_entries)
        return HttpResponse(json.dumps({
            'habit': serialized_habit,
            'habit_entries': serialized_habit_entries
        }))

    # Delete habit
    elif request.method == 'DELETE':
        if habit is None:
            return HttpResponse(status=403)

        habit.delete()
        
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

        habit = Habit(
            user=current_user,
            name=name,
            send_text=send_text,
            send_time_utc=send_time_utc,
            response_type=response_type
        )
        habit.save()

        # Tell the user that a goal was created
        habit_creation_message = "Congrats, let's help you build this habit :). I'll ask you '" + send_text + "' everyday at " + send_time_utc + " UTC."
        send_api_helper.send_basic_text_message(fbid, habit_creation_message)
        message_log.log_message('habit_creation_message', current_user, habit_creation_message, None)

        return HttpResponse(status=200)
    # Error 404 Not Found
    else:
        return HttpResponse(status=403)

############################################
################# VIEWS ####################
############################################


# List all habits for a given user
def list(request, fbid):
    if not helper_util.user_exists(fbid):
        return HttpResponse(status=404)

    current_user = User.objects.get(fbid=fbid)
    if(not current_user):
        return HttpResponse("Invalid user")

    habits_list = Habit.objects.filter(user=current_user)
    serialized_response = serializers.serialize('json', habits_list)

    context = RequestContext(request, {
        'fbid': fbid,
        'habits': habits_list
    })
    template = loader.get_template('habits/list.html')
    return HttpResponse(template.render(context))


# Allow users to see entries for a given habit
def show(request, fbid, habit_id):
    habit = get_habit(habit_id)

    if not habit:
        return HttpResponse(status=403)

    habit_entries = HabitEntry.objects.filter(habit=habit).order_by('id')

    context = RequestContext(request, {
        'fbid': fbid,
        'habit': habit,
        'habit_entries': habit_entries
    })
    template = loader.get_template('habits/show.html')
    return HttpResponse(template.render(context))

# Allow users to add a habit
def add_habit_page(request, fbid):
    if not helper_util.user_exists(fbid):
        return HttpResponse(status=404)

    current_user = User.objects.get(fbid=fbid)
    if(not current_user):
        return HttpResponse("Invalid user")

    context = RequestContext(request, {
        'fbid': fbid
    })
    template = loader.get_template('habits/add.html')
    return HttpResponse(template.render(context))
