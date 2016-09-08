from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *
from main.utils import helper_util


def index(request):
    context = RequestContext(request, {})
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(context))


def learn_more(request):
    context = RequestContext(request, {})
    template = loader.get_template('main/learn_more.html')
    return HttpResponse(template.render(context))


def delete_users(request):
    all_users = User.objects.all()
    num_of_users_deleted = len(all_users)
    for u in all_users:
        u.delete()
    return HttpResponse("Deleted " + str(num_of_users_deleted) + " users!")

def delete_all(request):
    User.objects.all().delete()
    Habit.objects.all().delete()
    HabitEntry.objects.all().delete()
    ToDoTask.objects.all().delete()
    Message.objects.all().delete()

    return HttpResponse("Deleted all")

def dashboard(request, fbid):
    if not helper_util.user_exists(fbid):
        return HttpResponse(status=404)
    context = RequestContext(request, {})
    template = loader.get_template('main/dashboard.html')
    return HttpResponse(template.render(context))

def connect(request, fbid):
    if not helper_util.user_exists(fbid):
        return HttpResponse(status=404)
    user = User.objects.get(fbid=fbid)

    context = RequestContext(request, {
        'lyft_connected_flag' : user.rideshareinformation.lyft_connected_flag,
        'foursquare_connected_flag' : hasattr(user,'foursquareconnection') and user.foursquareconnection.is_connected_flag,
        'lyft_connected_flag' : hasattr(user,'lyftconnection') and user.lyftconnection.is_connected_flag,
        'uber_connected_flag' : hasattr(user, 'uberconnection') and user.uberconnection.is_connected_flag,
        'instagram_connected_flag' : hasattr(user, 'instagramconnection') and user.instagramconnection.is_connected_flag,
        'fitbit_connected_flag' : False, #hasattr(user, 'fitbitconnection') and user.fitbitconnection.is_connected_flag,
        'fbid' : user.fbid
        
        })
    template = loader.get_template('main/connect.html')
    return HttpResponse(template.render(context))
