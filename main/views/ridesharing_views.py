from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *
from main.utils import helper_util

def lyft_set_up(fbid):
    # Get current user
    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=404)

    return current_user.rideshareinformation.lyft_connected_flag

def uber_set_up(fbid):
    # Get current user
    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=404)

    return current_user.rideshareinformation.uber_connected_flag

def setup(request, fbid):

    lyft_connected_flag = lyft_set_up(fbid)
    uber_connected_flag = uber_set_up(fbid)

    # If ridesharing set up, show form to update information
    if lyft_connected_flag or uber_connected_flag:
        context = RequestContext(request, {
            'lyft_set_up_flag' : lyft_connected_flag,
            'uber_set_up_flag' : uber_connected_flag,
            'fbid' : fbid
            })
    # Else, allow user to set up ridesharing
    else:
        context = RequestContext(request, {
            'lyft_set_up_flag' : lyft_connected_flag,
            'uber_set_up_flag' : uber_connected_flag,
            'fbid' : fbid
            })
    template = loader.get_template('main/ridesharing_setup.html')
    return HttpResponse(template.render(context))


