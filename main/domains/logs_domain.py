from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import helper_util
import json
from main.utils import nlp

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'

# Global handler for anything logs related
def handle_logs_text(current_user, text, processed_text):
    print 'in handle_logs_text'
    print 'processed_text: ' + processed_text

    # Triggers asking what they want to log
    if processed_text == 'log':
        handle_log_listening(current_user, text, processed_text)
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

        # Log the entry
        entry_raw_text = log_entry_raw[1]

        if helper_util.is_number(entry_raw_text):
            handle_numeric_log_entry(current_user, entry_raw_text)
        else:
            handle_text_log_entry(current_user, entry_raw_text)
    # User responded to listening_message
    elif nlp.user_is_in_log_entry_state(current_user):
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

    text_log_entry = TextLogEntry(log=user_log, text_value=entry_text)
    text_log_entry.save()

    log_contexts = LogContext.objects.filter(log=user_log)

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

    for context in log_contexts:
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

    numeric_log_entry = NumericLogEntry(log=user_log, numeric_value=numeric_value)
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

    for context in log_contexts:
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
def handle_image_log_entry(current_user, entry_text):
    user_log = Log.find_or_create(current_user)

    image_log_entry = ImageLogEntry(log=user_log, image_value=image_value)
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

    for context in log_contexts:
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
    print 'in handle_log_listening'
    # Log response
    message_log.log_message(
            'log_trigger_listening_response',
            current_user,
            processed_text,
            None
        )

    # Send and log message
    log_listening_message = "I'm listening - reply with a number, text, or image!"
    send_api_helper.send_basic_text_message(
            current_user.fbid,
            log_listening_message
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
    recent_entry = TextLogEntry.objects.filter(
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
            
