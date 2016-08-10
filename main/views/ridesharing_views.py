from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from main.models import *
from main.utils import helper_util
from main.api import google_geocode

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

    # Get current_user
    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=200)

    rideshare_information = current_user.rideshareinformation

    # If ridesharing set up, show form to update information
    if lyft_connected_flag or uber_connected_flag:
        context = RequestContext(request, {
            'lyft_set_up_flag' : lyft_connected_flag,
            'uber_set_up_flag' : uber_connected_flag,
            'fbid' : fbid,
            'home_address' : rideshare_information.current_home_address,
            'work_address' : rideshare_information.current_work_address
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


# REST Endpoints
def rideshare_information(request):
    if request.method == 'POST':
        home_address = request.POST['home_address']
        work_address = request.POST['work_address']
        fbid = request.POST['fbid']

        # Geocode
        (home_formatted_address, home_lat, home_lng) = google_geocode.geocode_address(home_address)

        (work_formatted_address, work_lat, work_lng) = google_geocode.geocode_address(work_address)

        # Get current user
        if helper_util.user_exists(fbid):
            current_user = User.objects.get(fbid=fbid)
        else:
            return HttpResponse(status=200)

        rideshare_information = current_user.rideshareinformation

        # Update rideshare information
        rideshare_information.home_lat = home_lat
        rideshare_information.work_lat = work_lat
        rideshare_information.home_lng = home_lng
        rideshare_information.work_lng = work_lng
        rideshare_information.current_home_address = home_formatted_address
        rideshare_information.current_work_address = work_formatted_address

        rideshare_information.save()

        # Update rideshare information
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)










