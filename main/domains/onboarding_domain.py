from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper, fb_profile_helper
from main.models import *
from main.utils import constants

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

    # If user doesn't exist, create user
    p = Profile(
        fbid=fbid,
        utc_offset=timezone,
        send_reminders_flag=True,
        reminder_settings=0,
        first_name=first_name,
        last_name=last_name
    )
    p.save()

    # Create default categories
    user_log = Log.find_or_create(p)
    thoughts_context = LogContext(log=user_log, context_name="Thoughts")
    thoughts_context.save()

    links_context = LogContext(log=user_log, context_name="Links")
    links_context.save()

    read_watch_category = LogContext(log=user_log, context_name="Read/Watch")
    read_watch_category.save()

    # Send user intro message
    welcome_message = "Hey " + first_name + "! LastThought is a bot that helps you store your thoughts!"
    send_api_helper.send_basic_text_message(fbid, welcome_message)
    message_log.log_message('welcome_message', p, welcome_message, None)

    # Send "learn more" message
    send_learn_more_message(p)

    # Send get started message
    send_get_started_message(p)


def send_learn_more_message(profile):
    learn_more_message = "It's simple - anytime you want to remember something, whether it be an idea, photo, link, or journal entry, simply send it to me and I'll store it for you!"
    send_api_helper.send_basic_text_message(profile.fbid, learn_more_message)
    message_log.log_message(
        'learn_more_message',
        profile,
        learn_more_message,
        None
    )


def send_get_started_message(profile):
    get_started_message = "Let's get started! Start by either sending me a thought you want to remember, something you want to read/watch, or a link to save."
    send_api_helper.send_basic_text_message(profile.fbid, get_started_message)
    message_log.log_message(
        'get_started_message',
        profile,
        get_started_message,
        None
    )


def send_categories_explanation_message(profile):
    categories_explanation_message = "If you want, you can categorize each thought that you send to me! You can then view your thoughts by category on our site. Try categorizing it as a Thought:"
    send_api_helper.send_basic_text_message(
        profile.fbid,
        categories_explanation_message
    )
    message_log.log_message(
        'categories_explanation_message',
        profile,
        categories_explanation_message,
        None
    )


def send_almost_done_message(profile):
    # Send message explaining
    explain_link_message = 'You\'re almost done! Tap the button below to sign up and view your stored thoughts:'
    send_api_helper.send_basic_text_message(profile.fbid, explain_link_message)
    message_log.log_message(
        'explain_link_message',
        profile,
        explain_link_message,
        None
    )


def send_create_account_message(profile):
    # Send account linking message
    sign_up_message = 'Sign Up!'
    send_api_helper.send_account_link_message(profile.fbid, sign_up_message)
    message_log.log_message(
        'sign_up_message',
        profile,
        sign_up_message,
        None
    )


def send_finished_onboarding_message(profile):
    finished_onboarding_message = "You're all set! You can view your thoughts anytime by tapping View Thoughts in the bottom left menu or go to {}".format(constants.BASE_URL)
    send_api_helper.send_basic_text_message(
        profile.fbid,
        finished_onboarding_message
    )
    message_log.log_message(
        'finished_onboarding_message',
        profile,
        finished_onboarding_message,
        None
    )


def send_share_message(profile):
    share_message = 'Send LastThought to your friends so they can also keep and remember their thoughts!'
    send_api_helper.send_share_message(profile.fbid, share_message)
    message_log.log_message(
        'share_message',
        profile,
        share_message,
        None
    )
