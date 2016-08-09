from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import constants, helper_util
from django.http import HttpResponse, HttpResponseRedirect
from main.api import lyft

def handle(current_user, text, processed_text):
    # Log ride response
    message_log.log_message('ridesharing_setup_response', current_user, text, None)

    # Send the ridesharing message and url
    ridesharing_setup_message = "Setup ridesharing:"
    send_api_helper.send_button_message(current_user.fbid, ridesharing_setup_message, [{
            'type': 'web_url',
            'url': constants.BASE_HEROKU_URL + '/users/'+str(current_user.fbid)+'/setup_ridesharing',
            'title': 'Go'
        }])
    message_log.log_message('ridesharing_setup_message', current_user, ridesharing_setup_message, None)
    
def lyft_redirect(request):
    print request.GET

    # Get query params
    authorization_code = request.GET['code']
    fbid = request.GET['state']

    # Get current user
    if helper_util.user_exists(fbid):
        current_user = User.objects.get(fbid=fbid)
    else:
        return HttpResponse(status=404)

    # Get access_token and refresh_token
    (access_token, refresh_token) = lyft.retrieve_access_token(authorization_code)

    print access_token
    print '-----'
    print refresh_token
    
    # Update Rideshare information
    rideshare_information = current_user.rideshareinformation
    rideshare_information.lyft_access_token = access_token
    rideshare_information.lyft_refresh_token = refresh_token
    rideshare_information.lyft_connected_flag = True
    rideshare_information.save()

    # Redirect to ridesharing_setup page
    return HttpResponseRedirect("/ridesharing_setup")

def lyft_webhook(request):
    # Todo
    print request.GET

def uber_webhook(request):
    # Todo
    x = 1
