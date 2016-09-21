from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper, fb_profile_helper
from main.models import *

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

def create_new_user(fbid):
    # If user doesn't exist, create user
    u = Profile(fbid=fbid)
    u.save()

    # Get user profile information
    (
        first_name,
        last_name,
        profile_pic,
        locale,
        timezone,
        gender
        ) = fb_profile_helper.get_user_profile_data(fbid)

    # Send user intro message
    welcome_message = "Hey "+ first_name +"! Nice to meet you. I'm Jarvis, here to help you keep a diary of your life!"
    send_api_helper.send_basic_text_message(fbid, welcome_message)
    message_log.log_message('welcome_message', u, welcome_message, None)

    # Send "learn more" message
    send_learn_more_message(u)

    # Send get started message
    send_get_started_message(u)


def send_learn_more_message(current_user):
    learn_more_message = "It's super simple - anytime you want to remember something, whether it be a thought, photo, or video, simply send it to me and I'll store it for you!"
    send_api_helper.send_button_message(current_user.fbid, learn_more_message, [
            {
                'type': 'web_url',
                'url': 'http://userdatagraph.herokuapp.com/learn_more',
                'title': 'Learn More'
            }
        ])
    message_log.log_message('learn_more_message', current_user, learn_more_message, None)

def send_get_started_message(current_user):
    get_started_message = "Let's get your diary started with a selfie! Tap the camera below this message, and send me a selfie :)"
    send_api_helper.send_basic_text_message(current_user.fbid, get_started_message)
    message_log.log_message('get_started_message', current_user, get_started_message, None)

def send_categories_explanation_message(current_user):
    categories_explanation_message = "Want to keep track of your thoughts, funny pictures, and longer reflections all at once? No worry - I can also help you categorize your diary entries! Try it out:"
    send_api_helper.send_basic_text_message(current_user.fbid, categories_explanation_message)
    message_log.log_message('categories_explanation_message', current_user, categories_explanation_message, None)

def send_create_account_message(current_user):

    # Send message explaining
    explain_link_message = 'You\'re almost done. All you need to do is create an account so you can view your diary on the web or on your phone. Create an account here:'
    send_api_helper.send_basic_text_message(current_user.fbid, explain_link_message)
    message_log.log_message('explain_link_message', current_user, explain_link_message, None)

    # Send account linking message
    sign_up_message = 'Sign Up!'
    send_api_helper.send_account_link_message(current_user.fbid, sign_up_message)
    message_log.log_message('sign_up_message', current_user, sign_up_message, None)

def send_finished_onboarding_message(current_user):
    finished_onboarding_message = "Great - you can now view your diary any time by tapping View Diary in the menu or going to https://userdatagraph.herokuapp.com"
    send_api_helper.send_basic_text_message(current_user.fbid, finished_onboarding_message)
    message_log.log_message('finished_onboarding_message', current_user, finished_onboarding_message, None)

