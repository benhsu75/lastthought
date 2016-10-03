from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import helper_util, constants
import json
from main.utils import nlp
import boto3
import requests
from PIL import Image
import random
from main.domains import onboarding_domain
import datetime
from django.utils import timezone


# Global handler for anything logs related
def handle_logs_text(current_profile, text, processed_text):
    # Convert to UTF-8 (handles emojis)
    processed_text = processed_text.encode('utf-8')

    print 'Processing Text: ' + processed_text

    # User is adding new context
    if nlp.user_is_in_log_context_prompt_state(current_profile):
        add_and_apply_new_context(current_profile, text)
    # User is logging text or a number
    else:
        # Log the entry
        entry_raw_text = text

        if helper_util.is_number(entry_raw_text):
            numeric_value = float(entry_raw_text)

            handle_numeric_log_entry(current_profile, entry_raw_text)
        else:
            handle_text_log_entry(current_profile, entry_raw_text)


# Handles a text log entry
def handle_text_log_entry(current_profile, entry_text):
    user_log = Log.find_or_create(current_profile)

    num_log_entries = len(LogEntry.objects.filter(log=user_log))

    # Check if text log entry is too long (over 10000)
    TEXT_MAX_LENGTH = 10000
    if len(entry_text) > TEXT_MAX_LENGTH:
        send_log_too_long_message(current_profile)
        return

    text_log_entry = TextLogEntry(
        log=user_log,
        text_value=entry_text,
        entry_type=0,
        occurred_at=timezone.now()
    )
    text_log_entry.save()

    num_log_entries = len(LogEntry.objects.filter(log=user_log))

    # Ask the user to apply a context
    send_context_message(current_profile, "text", text_log_entry.id)


# Handles a numeric log entry
def handle_numeric_log_entry(current_profile, numeric_value):
    user_log = Log.find_or_create(current_profile)

    numeric_log_entry = NumericLogEntry(
        log=user_log,
        numeric_value=numeric_value,
        entry_type=1,
        occurred_at=datetime.datetime.now()
    )
    numeric_log_entry.save()

    # Ask the user to apply a context
    send_context_message(current_profile, "numeric", numeric_log_entry.id)


# Handles an image entry
def handle_image_log_entry(current_profile, image_url):
    user_log = Log.find_or_create(current_profile)

    # Download image from FB
    print 'DOWNLOADING IMAGE FROM FB'

    from StringIO import StringIO

    image_response = requests.get(image_url)
    # image_response.raw.decode_content = True
    # handle spurious Content-Encoding
    im = Image.open(StringIO(image_response.content))
    image_width, image_height = im.size

    # Upload to S3
    print 'UPLOADING TO S3'
    s3 = boto3.resource('s3')
    random_id = str(current_profile.fbid) + '-' + str(random.getrandbits(128))
    image_file_name = random_id + '.jpg'
    # fp = StringIO(im)
    s3.Bucket('userdatagraph-images').put_object(
        Key=image_file_name,
        Body=StringIO(image_response.content)
    )

    # Get Url and set image_url
    uploaded_image_url = 'https://s3.amazonaws.com/userdatagraph-images/{}'.format(image_file_name)
    print 'GOT THE NEW URL AS: ' + uploaded_image_url

    image_log_entry = ImageLogEntry(
        log=user_log,
        image_url=uploaded_image_url,
        entry_type=2,
        image_width=image_width,
        image_height=image_height,
        occurred_at=datetime.datetime.now()
    )
    image_log_entry.save()

    # Ask the user to apply a context
    send_context_message(current_profile, "image", image_log_entry.id)


# Helper method that asks the user to categorize their diary entry
def send_context_message(current_profile, entry_type, entry_id):

    # If first diary entry, then explain to user how categories work
    user_log = Log.find_or_create(current_profile)
    num_log_entries = len(LogEntry.objects.filter(log=user_log))
    print "num_log_entries " + str(num_log_entries)
    if num_log_entries == 1:
        onboarding_domain.send_categories_explanation_message(current_profile)

    # Send message to user to allow them to categorize their diary entry
    user_log = Log.find_or_create(current_profile)

    log_contexts = LogContext.objects.filter(
        log=user_log
    ).order_by('context_name')

    quick_replies = []

    count = 0
    for context in log_contexts:
        count += 1

        if count <= 8:
            # Edit
            payload = json.dumps({
                "state": "log_context_response",
                "log_context_id": context.id,
                "entry_type": entry_type,
                "log_entry_id": entry_id
            })
            quick_replies.append({
                "content_type": "text",
                "title": context.context_name,
                "payload": payload
            })

    quick_replies.append({
        "content_type": "text",
        "title": "Add new category",
        "image_url": "http://i.imgur.com/x7TulFM.png",
        "payload": json.dumps({
            "state": "log_context_response",
            "entry_type": entry_type,
            "add_new_context_flag": 1,
            "log_entry_id": entry_id
        })
    })

    add_context_message = "Categorize your diary entry:"
    send_api_helper.send_quick_reply_message(
        current_profile.fbid,
        add_context_message,
        quick_replies
    )
    message_log.log_message(
        'log_add_context_message',
        current_profile,
        add_context_message,
        None
    )


def send_max_number_categories_message(current_profile):
    # Send message explaining
    max_number_categories_message = 'You already have the maximum of 8 categories. We\'ve saved your thought, but to add a new category, first go to our website and delete an existing category.'
    send_api_helper.send_button_message(
        current_profile.fbid,
        max_number_categories_message,
        [{
            'type': 'web_url',
            'url': constants.BASE_URL,
            'title': 'View Thoughts',
            "messenger_extensions": True
        }]
    )
    message_log.log_message(
        'max_number_categories_message',
        current_profile,
        max_number_categories_message,
        None
    )


def send_category_name_too_long_message(current_profile):
    # Send message explaining
    category_name_too_long_message = 'Please try again'
    send_api_helper.send_basic_text_message(current_profile.fbid)
    message_log.log_message(
        'category_name_too_long_message',
        current_profile,
        category_name_too_long_message,
        None
    )


# Adds a new context based on the user response and applies
# that context to the log
def add_and_apply_new_context(current_profile, text):
    message_log.log_message(
        'log_new_context_response',
        current_profile,
        text,
        None
    )

    user_log = Log.objects.filter(profile=current_profile)[0]

    # Check how many categories the user has
    categories = LogContext.objects.filter(log=user_log)

    # Category has max_length
    MAX_LENGTH = 15
    if len(text) > MAX_LENGTH:
        message_text = "That's too long, please enter a category name shorter than {} characters:".format(MAX_LENGTH)
        send_ask_for_category_name_message(current_profile, message_text)
        return

    context = LogContext(log=user_log, context_name=text)
    context.save()

    # Get the right type of log entry
    recent_entry = LogEntry.objects.filter(
        log=user_log
    ).order_by('-created_at')[0]
    recent_entry.log_context = context
    recent_entry.save()

    message_text = "Thought stored and new category created (y)"
    send_category_applied_message(current_profile, message_text)

    # Get user to create account
    if not helper_util.user_has_created_account(current_profile):
        onboarding_domain.send_almost_done_message(current_profile)
        onboarding_domain.send_create_account_message(current_profile)


# Applies an existing context to the log
def apply_context_to_log(current_profile, text, payload):
    message_log.log_message(
        'log_context_response',
        current_profile,
        text,
        None
    )

    if "log_context_id" in payload:
        # Get log entry
        entry_type = payload['entry_type']
        entry_id = payload['log_entry_id']

        try:
            if entry_type == 'text':
                log_entry = TextLogEntry.objects.get(id=entry_id)
            elif entry_type == 'numeric':
                log_entry = NumericLogEntry.objects.get(id=entry_id)
            elif entry_type == 'image':
                log_entry = ImageLogEntry.objects.get(id=entry_id)
            else:
                # error
                return
        except (
            TextLogEntry.DoesNotExist,
            NumericLogEntry.DoesNotExist,
            ImageLogEntry.DoesNotExist
        ):
            # Tell the user that the log entry was deleted
            send_thought_was_deleted_message(current_profile)
            return

        # Get context
        context = LogContext.objects.get(id=payload["log_context_id"])
        log_entry.log_context = context
        log_entry.save()

        

        # If this is the first message, also tell user they don't have to categorize every thought
        user_log = Log.find_or_create(current_profile)
        if len(LogEntry.objects.filter(log=user_log)) == 1:
            message_text = "Thought stored (y). In the future, you can also not categorize a thought by simply not responding, but we'll still keep your thought" 
        else:
            message_text = "Thought stored (y)"

        send_category_applied_message(current_profile, message_text)

        # Get user to create account
        if not helper_util.user_has_created_account(current_profile):
            onboarding_domain.send_almost_done_message(current_profile)
            onboarding_domain.send_create_account_message(current_profile)

    elif "add_new_context_flag" in payload:

        user_log = Log.objects.filter(profile=current_profile)[0]

        # Check how many categories the user has
        categories = LogContext.objects.filter(log=user_log)

         # Tell the user they can't add anymore
        if len(categories) >= 8:
            send_max_number_categories_message(current_profile)
            return

        # Confirm if log still exists - if it doesn't, tell user
        entry_id = payload['log_entry_id']

        # Get log entry
        entry_type = payload['entry_type']
        entry_id = payload['log_entry_id']

        try:
            if entry_type == 'text':
                log_entry = TextLogEntry.objects.get(id=entry_id)
            elif entry_type == 'numeric':
                log_entry = NumericLogEntry.objects.get(id=entry_id)
            elif entry_type == 'image':
                log_entry = ImageLogEntry.objects.get(id=entry_id)
            else:
                # error
                return
        except (
            TextLogEntry.DoesNotExist,
            NumericLogEntry.DoesNotExist,
            ImageLogEntry.DoesNotExist
        ):
            # Tell the user that the log entry was deleted
            send_thought_was_deleted_message(current_profile)
            return

        message_text = "What is the name of the category you want to add?"
        send_ask_for_category_name_message(current_profile, message_text)

    elif "no_context_flag" in payload:

        send_no_category_message(current_profile)

        # Get user to create account
        if not helper_util.user_has_created_account(current_profile):
            onboarding_domain.send_almost_done_message(current_profile)
            onboarding_domain.send_create_account_message(current_profile)


# MESSAGE HELPER METHODS
def send_category_applied_message(profile, text):
    successful_context_message = text
    send_api_helper.send_basic_text_message(
        profile.fbid,
        successful_context_message
    )
    message_log.log_message(
        'log_successful_context_message',
        profile,
        successful_context_message,
        None
    )


def send_thought_was_deleted_message(profile):
    thought_was_deleted_message = (
        "That thought was deleted so it can't be categorized anymore"
    )
    send_api_helper.send_basic_text_message(
        profile.fbid,
        thought_was_deleted_message
    )
    message_log.log_message(
        'thought_was_deleted_message',
        profile,
        thought_was_deleted_message,
        None
    )


def send_no_category_message(profile):
    log_confirm_message = (
        "I logged this for you!"
    )
    send_api_helper.send_basic_text_message(
        profile.fbid,
        log_confirm_message
    )
    message_log.log_message(
        'log_confirm_message',
        profile,
        log_confirm_message,
        None
    )


def send_ask_for_category_name_message(profile, new_context_message):
    # Create "Cancel" quick reply
    quick_replies = []
    quick_replies.append({
        "content_type": "text",
        "title": "Cancel",
        "payload": json.dumps({
            "state": "cancel_new_category"
        })
    })

    # Send message
    send_api_helper.send_quick_reply_message(
        profile.fbid,
        new_context_message,
        quick_replies
    )
    message_log.log_message(
        'log_new_context_message',
        profile,
        new_context_message,
        None
    )


def send_log_too_long_message(current_profile):
    log_too_long_message = "We cannot store that much text! Please enter less than 10,000 characters!"
    send_api_helper.send_basic_text_message(
        current_profile.fbid,
        log_too_long_message
    )
    message_log.log_message(
        'log_too_long_message',
        current_profile,
        log_too_long_message,
        None
    )


def send_successful_new_category_cancel(profile):
    send_successful_new_category_cancel = "OK - we saved your thought but no category was applied."
    send_api_helper.send_basic_text_message(
        profile.fbid,
        send_successful_new_category_cancel
    )
    message_log.log_message(
        'send_successful_new_category_cancel',
        profile,
        send_successful_new_category_cancel,
        None
    )
