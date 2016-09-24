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

    print 'in handle_logs_text'
    print 'processed_text: ' + processed_text

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

# Helper method to send message for user to view logs
def send_view_logs_message(current_profile):
    # Send user message linking to log
    log_view_message = (
        "Click to view your logs"
    )
    send_api_helper.send_button_message(current_profile.fbid, log_view_message, [
        {
            'type': 'web_url',
            'url': constants.BASE_HEROKU_URL + '/users/'+str(current_profile.fbid)+'/logs',
            'title': 'See Logs'    
        }
    ])
    message_log.log_message(
        'log_view_message',
        current_profile,
        log_view_message,
        None
    )

# Handles a text log entry
def handle_text_log_entry(current_profile, entry_text):
    user_log = Log.find_or_create(current_profile)

    num_log_entries = len(LogEntry.objects.filter(log=user_log))

    text_log_entry = TextLogEntry(log=user_log, text_value=entry_text, entry_type=0, occurred_at=timezone.now())
    text_log_entry.save()

    num_log_entries = len(LogEntry.objects.filter(log=user_log))

    # Ask the user to apply a context
    send_context_message(current_profile, "text", text_log_entry.id)

# Handles a numeric log entry
def handle_numeric_log_entry(current_profile, numeric_value):
    user_log = Log.find_or_create(current_profile)

    numeric_log_entry = NumericLogEntry(log=user_log, numeric_value=numeric_value, entry_type=1, occurred_at=datetime.datetime.now())
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
    # image_response.raw.decode_content = True # handle spurious Content-Encoding
    im = Image.open(StringIO(image_response.content))
    image_width, image_height = im.size

    # Upload to S3
    print 'UPLOADING TO S3'
    s3 = boto3.resource('s3')
    random_id = str(current_profile.fbid) + '-' + str(random.getrandbits(128))
    image_file_name = random_id + '.jpg'
    # fp = StringIO(im)
    s3.Bucket('userdatagraph-images').put_object(Key=image_file_name, Body=StringIO(image_response.content))


    # Get Url and set image_url
    uploaded_image_url = 'https://s3.amazonaws.com/userdatagraph-images/' + image_file_name
    print 'GOT THE NEW URL AS: ' + uploaded_image_url

    image_log_entry = ImageLogEntry(log=user_log, image_url=uploaded_image_url, entry_type=2, image_width=image_width, image_height=image_height, occurred_at=datetime.datetime.now())
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

    log_contexts = LogContext.objects.filter(log=user_log).order_by('context_name')

    quick_replies = [{
        "content_type": "text",
        "title": "None",
        "payload": json.dumps({
            "state": "log_context_response",
            "entry_type": entry_type,
            "no_context_flag" : 1,
            "log_entry_id": entry_id
        })
    }]

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
        "title": "Add a new category",
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

# Adds a new context based on the user response and applies that context to the log
def add_and_apply_new_context(current_profile, text):
    message_log.log_message(
        'log_new_context_response',
        current_profile,
        text,
        None
    )

    user_log = Log.objects.filter(user=current_profile)[0]
    context = LogContext(log=user_log, context_name=text)
    context.save()

    # Get the right type of log entry
    recent_entry = LogEntry.objects.filter(
        log=user_log
    ).order_by('-created_at')[0]
    recent_entry.log_context = context
    recent_entry.save()

    successful_context_message = (
        "\"" + context.context_name + "\""
        + " was applied to your log entry."
    )
    send_api_helper.send_basic_text_message(
        current_profile.fbid,
        successful_context_message
    )
    message_log.log_message(
        'log_successful_context_message',
        current_profile,
        successful_context_message,
        None
    )

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

        if entry_type == 'text':
            log_entry = TextLogEntry.objects.get(id=entry_id)
        elif entry_type == 'numeric':   
            log_entry = NumericLogEntry.objects.get(id=entry_id)
        elif entry_type == 'image':
            log_entry = ImageLogEntry.objects.get(id=entry_id)
        else:
            # error
            return

        # Get context
        context = LogContext.objects.get(id=payload["log_context_id"])
        log_entry.log_context = context
        log_entry.save()

        successful_context_message = (
            "\"" + context.context_name + "\""
            + " was applied to your diary entry."
        )
        send_api_helper.send_basic_text_message(
            current_profile.fbid,
            successful_context_message
        )
        message_log.log_message(
            'log_successful_context_message',
            current_profile,
            successful_context_message,
            None
        )

        # Get user to create account
        if not helper_util.user_has_created_account(current_profile):
            onboarding_domain.send_almost_done_message(current_profile)
            onboarding_domain.send_create_account_message(current_profile)

    elif "add_new_context_flag" in payload:
        new_context_message = (
            "What is the name of the category you want to add?"
        )
        send_api_helper.send_basic_text_message(
            current_profile.fbid,
            new_context_message
        )
        message_log.log_message(
            'log_new_context_message',
            current_profile,
            new_context_message,
            None
        )
    elif "no_context_flag" in payload:
        log_confirm_message = (
            "I logged this for you!"
        )
        send_api_helper.send_basic_text_message(
            current_profile.fbid,
            log_confirm_message
        )
        message_log.log_message(
            'log_confirm_message',
            current_profile,
            log_confirm_message,
            None
        )

        # Get user to create account
        if not helper_util.user_has_created_account(current_profile):
            onboarding_domain.send_almost_done_message(current_profile)
            onboarding_domain.send_create_account_message(current_profile)

