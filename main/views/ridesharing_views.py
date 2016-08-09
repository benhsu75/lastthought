from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *
from main.utils import helper_util

def ridesharing_set_up(fbid):
    # Get current user
    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=404)

    return current_user.rideshareinformation.connected_flag

def setup(request, fbid):

    # If ridesharing set up, show form to update information
    if ridesharing_set_up(fbid):
        context = RequestContext(request, {
            'ridesharing_set_up_flag' : True,
            'fbid' : fbid
            })
    # Else, allow user to set up ridesharing
    else:
        context = RequestContext(request, {
            'ridesharing_set_up_flag' : False,
            'fbid' : fbid
            })
    template = loader.get_template('main/ridesharing_setup.html')
    return HttpResponse(template.render(context))


