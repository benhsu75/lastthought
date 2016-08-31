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

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

# Global handler for anything logs related
def handle_logs_text(current_user, text, processed_text, no_trigger_flag=False):
    print 'in handle_logs_text'
    print 'processed_text: ' + processed_text

    # Triggers asking what they want to log
    if processed_text == 'log':
        handle_log_listening(current_user, text, processed_text)
    elif processed_text == 'see logs':
        # Send user message linking to log
        log_view_message = (
            "Click to view your logs"
        )
        send_api_helper.send_button_message(current_user.fbid, log_view_message, [
            {
                'type': 'web_url',
                'url': constants.BASE_HEROKU_URL + '/users/'+str(current_user.fbid)+'/logs',
                'title': 'See Logs'    
            }
        ])
        message_log.log_message(
            'log_view_message',
            current_user,
            log_view_message,
            None
        )

    # Triggers asking what context
    elif processed_text.startswith('log:'):
        # Log response
        message_log.log_message(
            'log_new_entry_response',
            current_user,
            text,
            None
        )

        # Parse out 'log:'
        log_entry_raw = text.split(None, 1)

        # If incorrect format
        if len(log_entry_raw) < 2:
            log_invalid_trigger_message = ("Looks like an empty log entry! "
                 "Type in \"log: [your log entry]\" to log something.")
            send_api_helper.send_basic_text_message(
                current_user.fbid,
                log_invalid_trigger_message
            )
            message_log.log_message(
                'log_invalid_trigger_message',
                current_user,
                log_invalid_trigger_message,
                None
            )
            return

        # Log the entry
        entry_raw_text = log_entry_raw[1]

        if helper_util.is_number(entry_raw_text):
            handle_numeric_log_entry(current_user, entry_raw_text)
        else:
            handle_text_log_entry(current_user, entry_raw_text)
    # User responded to listening_message
    elif no_trigger_flag or nlp.user_is_in_log_entry_state(current_user):
        # Log the entry
        entry_raw_text = text

        if helper_util.is_number(entry_raw_text):
            numeric_value = float(entry_raw_text)

            handle_numeric_log_entry(current_user, entry_raw_text)
        else:
            handle_text_log_entry(current_user, entry_raw_text)
    else:
        add_and_apply_new_context(current_user, text)

# Handles a text log entry
def handle_text_log_entry(current_user, entry_text):
    user_log = Log.find_or_create(current_user)

    text_log_entry = TextLogEntry(log=user_log, text_value=entry_text, entry_type=0)
    text_log_entry.save()

    log_contexts = LogContext.objects.filter(log=user_log).order_by('context_name')

    quick_replies = [{
        "content_type": "text",
        "title": "None",
        "payload": json.dumps({
            "state": "log_context_response",
            "entry_type": "text",
            "no_context_flag" : 1,
            "log_entry_id": text_log_entry.id
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
                "entry_type": "text",
                "log_entry_id": text_log_entry.id
            })
            quick_replies.append({
                "content_type": "text",
                "title": context.context_name,
                "payload": payload
            })

    quick_replies.append({
        "content_type": "text",
        "title": "Add a new context",
        "payload": json.dumps({
            "state": "log_context_response",
            "entry_type": "text",
            "add_new_context_flag": 1,
            "log_entry_id": text_log_entry.id
        })
    })

    add_context_message = "Add a context to your log entry:"
    send_api_helper.send_quick_reply_message(
        current_user.fbid,
        add_context_message,
        quick_replies
    )
    message_log.log_message(
        'log_add_context_message',
        current_user,
        add_context_message,
        None
    )

# Handles a numeric log entry
def handle_numeric_log_entry(current_user, numeric_value):
    user_log = Log.find_or_create(current_user)

    numeric_log_entry = NumericLogEntry(log=user_log, numeric_value=numeric_value, entry_type=1)
    numeric_log_entry.save()

    log_contexts = LogContext.objects.filter(log=user_log)

    quick_replies = [{
        "content_type": "text",
        "title": "None",
        "payload": json.dumps({
            "state": "log_context_response",
            "entry_type": "numeric",
            "no_context_flag" : 1,
            "log_entry_id": numeric_log_entry.id
        })
    }]

    count = 0
    for context in log_contexts:
        count += 1

        if count <= 8:
            payload = json.dumps({
                "state": "log_context_response",
                "log_context_id": context.id,
                "entry_type": "numeric",
                "log_entry_id": numeric_log_entry.id
            })
            quick_replies.append({
                "content_type": "text",
                "title": context.context_name,
                "payload": payload
            })

    quick_replies.append({
        "content_type": "text",
        "title": "Add a new context",
        "payload": json.dumps({
            "state": "log_context_response",
            "add_new_context_flag": 1,
            "entry_type": "numeric",
            "log_entry_id": numeric_log_entry.id
        })
    })

    add_context_message = "Add a context to your log entry:"
    send_api_helper.send_quick_reply_message(
        current_user.fbid,
        add_context_message,
        quick_replies
    )
    message_log.log_message(
        'log_add_context_message',
        current_user,
        add_context_message,
        None
    )

# Handles an image entry
def handle_image_log_entry(current_user, image_url):
    user_log = Log.find_or_create(current_user)

    # Download image from FB
    print 'DOWNLOADING IMAGE FROM FB'
    image_response = requests.get(image_url)
    r.raw.decode_content = True # handle spurious Content-Encoding
    im = Image.open(r.raw)

    # Upload to S3
    print 'UPLOADING TO S3'
    s3 = boto3.resource('s3')
    random_id = current_user.fbid + '-' + random.getrandbits(128)
    image_file_name = random_id + '.png'
    s3.Bucket('userdatagraph-images').put_object(Key=image_file_name, Body=im)


    # Get Url and set image_url
    uploaded_image_url = 'https://userdatagraph.s3.amazonaws.com/' + image_file_name
    print 'GOT THE NEW URL AS: ' + uploaded_image_url

    image_log_entry = ImageLogEntry(log=user_log, image_url=image_url, entry_type=2)
    image_log_entry.save()

    log_contexts = LogContext.objects.filter(log=user_log)

    quick_replies = [{
        "content_type": "text",
        "title": "None",
        "payload": json.dumps({
            "state": "log_context_response",
            "entry_type": "image",
            "no_context_flag" : 1,
            "log_entry_id": image_log_entry.id
        })
    }]

    count = 0
    for context in log_contexts:
        count += 1

        if count <= 8:
            payload = json.dumps({
                "state": "log_context_response",
                "log_context_id": context.id,
                "entry_type": "image",
                "log_entry_id": image_log_entry.id
            })
            quick_replies.append({
                "content_type": "text",
                "title": context.context_name,
                "payload": payload
            })

    quick_replies.append({
        "content_type": "text",
        "title": "Add a new context",
        "payload": json.dumps({
            "state": "log_context_response",
            "entry_type": "image",
            "add_new_context_flag": 1,
            "log_entry_id": image_log_entry.id
        })
    })

    add_context_message = "Add a context to your log entry:"
    send_api_helper.send_quick_reply_message(
        current_user.fbid,
        add_context_message,
        quick_replies
    )
    message_log.log_message(
        'log_add_context_message',
        current_user,
        add_context_message,
        None
    )

# Handles the case where user says "log"
def handle_log_listening(current_user, text, processed_text):
    # Log response
    message_log.log_message(
            'log_trigger_listening_response',
            current_user,
            processed_text,
            None
        )

    # Send and log message
    log_listening_message = "I'm listening - reply with a number, text, or image!"
    quick_replies = [{
        "content_type": "text",
        "title": "Cancel",
        "payload": json.dumps({
            "state": "cancel_log"
        })
    }]

    send_api_helper.send_quick_reply_message(
        current_user.fbid,
        log_listening_message,
        quick_replies
    )
    message_log.log_message(
            'log_listening_message',
            current_user,
            log_listening_message,
            None
        )
# Adds a new context based on the user response and applies that context to the log
def add_and_apply_new_context(current_user, text):
    message_log.log_message(
        'log_new_context_response',
        current_user,
        text,
        None
    )


    user_log = Log.objects.filter(user=current_user)[0]
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
        current_user.fbid,
        successful_context_message
    )
    message_log.log_message(
        'log_successful_context_message',
        current_user,
        successful_context_message,
        None
    )


# Applies an existing context to the log
def apply_context_to_log(current_user, text, payload):
    message_log.log_message(
        'log_context_response',
        current_user,
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
            + " was applied to your log entry."
        )
        send_api_helper.send_basic_text_message(
            current_user.fbid,
            successful_context_message
        )
        message_log.log_message(
            'log_successful_context_message',
            current_user,
            successful_context_message,
            None
        )
    elif "add_new_context_flag" in payload:
        new_context_message = (
            "What is the name of the context you want to add?"
        )
        send_api_helper.send_basic_text_message(
            current_user.fbid,
            new_context_message
        )
        message_log.log_message(
            'log_new_context_message',
            current_user,
            new_context_message,
            None
        )
    elif "no_context_flag" in payload:
        log_confirm_message = (
            "I logged this for you!"
        )
        send_api_helper.send_basic_text_message(
            current_user.fbid,
            log_confirm_message
        )
        message_log.log_message(
            'log_confirm_message',
            current_user,
            log_confirm_message,
            None
        )

def handle_cancel_log(current_user, text, payload):
    message_log.log_message(
        'cancel_log_response',
        current_user,
        text,
        None
    )

    cancel_log_message = 'k!'
    send_api_helper.send_basic_text_message(
        current_user.fbid,
        cancel_log_message
    )
    message_log.log_message(
        'cancel_log_message',
        current_user,
        cancel_log_message,
        None
    )
