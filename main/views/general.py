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
        'fitbit_connected_flag' : hasattr(user, 'fitbitconnection') and user.fitbitconnection.is_connected_flag,
        'gmail_connected_flag' : False,#hasattr(user, 'gmailconnection') and user.gmailconnection.is_connected_flag,
        'gcal_connected_flag' : False,#hasattr(user, 'gcalconnection') and user.gcalconnection.is_connected_flag,
        'gdrive_connected_flag' : False,#hasattr(user, 'gdriveconnection') and user.gdriveconnection.is_connected_flag,
        'facebook_connected_flag' : False,#hasattr(user, 'facebookconnection') and user.facebookconnection.is_connected_flag,
        'fbid' : user.fbid
        
        })
    template = loader.get_template('main/connect.html')
    return HttpResponse(template.render(context))
