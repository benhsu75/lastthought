from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper, fb_profile_helper
from main.models import *

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def create_new_user(fbid):

    # Get user profile information
    (
        first_name,
        last_name,
        profile_pic,
        locale,
        timezone,
        gender
        ) = fb_profile_helper.get_user_profile_data(fbid)

    print 'Timezone: ' + timezone

    # If user doesn't exist, create user
    p = Profile(fbid=fbid)
    p.save()

    # Send user intro message
    welcome_message = "Hey "+ first_name +"! LastThought is a bot that helps you keep track of the little things you want to remember!"
    send_api_helper.send_basic_text_message(fbid, welcome_message)
    message_log.log_message('welcome_message', p, welcome_message, None)

    # Send "learn more" message
    send_learn_more_message(p)

    # Send get started message
    send_get_started_message(p)

def send_learn_more_message(current_profile):
    learn_more_message = "It's simple - anytime you want to remember something, whether it be a journal entry, idea, photo, or link, simply send it to me and I'll store it for you!"
    send_api_helper.send_basic_text_message(current_profile.fbid, learn_more_message)
    message_log.log_message('learn_more_message', current_profile, learn_more_message, None)

def send_get_started_message(current_profile):
    get_started_message = "Let's get started! Tap the camera below this message and send me a selfie or tell me how you're feeling today!"
    send_api_helper.send_basic_text_message(current_profile.fbid, get_started_message)
    message_log.log_message('get_started_message', current_profile, get_started_message, None)

def send_categories_explanation_message(current_profile):
    categories_explanation_message = "Keeping track of thoughts, pictures, links, and more? After each thought you send, LastThought can also help you categorize your diary entries! Try it out:"
    send_api_helper.send_basic_text_message(current_profile.fbid, categories_explanation_message)
    message_log.log_message('categories_explanation_message', current_profile, categories_explanation_message, None)

def send_almost_done_message(current_profile):
    # Send message explaining
    explain_link_message = 'You\'re almost done. Tap the button below to sign up through Facebook so you can view your thoughts at any time:'
    send_api_helper.send_basic_text_message(current_profile.fbid, explain_link_message)
    message_log.log_message('explain_link_message', current_profile, explain_link_message, None)

def send_create_account_message(current_profile):
    # Send account linking message
    sign_up_message = 'Sign Up!'
    send_api_helper.send_account_link_message(current_profile.fbid, sign_up_message)
    message_log.log_message('sign_up_message', current_profile, sign_up_message, None)

def send_finished_onboarding_message(current_profile):
    finished_onboarding_message = "Thanks for signing up! You can view your thoughts at any time by tapping View Diary in the menu below or going to https://userdatagraph.herokuapp.com"
    send_api_helper.send_basic_text_message(current_profile.fbid, finished_onboarding_message)
    message_log.log_message('finished_onboarding_message', current_profile, finished_onboarding_message, None)

