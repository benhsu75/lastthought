from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import helper_util
import json

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'


def handle_logs_text(current_user, text):
    if text.split()[0].lower() == "log:":
        handle_log_entry(current_user, text)
    else:
        add_and_apply_new_context(current_user, text)


def handle_log_entry(current_user, text):
    user_log = Log.find_or_create(current_user)

    log_entry_raw = text.split(None, 1)
    if len(log_entry_raw) < 2:
        send_api_helper.send_basic_text_message(
            current_user.fbid,
            ("Looks like an empty log entry! "
             "Type in \"log: [your log entry]\" to log something.")
        )

    if helper_util.is_number(log_entry_raw[1]):
        # wait for context before saving
        pass
    else:
        entry_text = log_entry_raw[1]
        text_log_entry = TextLogEntry(log=user_log, text_value=entry_text)
        text_log_entry.save()

        message_log.log_message(
            'log_new_entry_response',
            current_user,
            text,
            None
        )

        log_contexts = LogContext.objects.filter(log=user_log)

        quick_replies = [{
            "content_type": "text",
            "title": "None",
            "payload": json.dumps({
                "state": "log_context_response",
                "log_entry_id": text_log_entry.id
            })
        }]

        for context in log_contexts:
            payload = json.dumps({
                "state": "log_context_response",
                "log_context_id": context.id,
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

    # need to deal with numeric/picture log entries later
    recent_entry = TextLogEntry.objects.filter(
        log=user_log
    ).order_by('-created_at')[0]
    recent_entry.log_context = context
    recent_entry.save()

    successful_context_message = (
        "\"" + context.context_name + "\""
        + "was applied to your log entry."
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


def apply_context_to_log(current_user, text, payload):
    message_log.log_message(
        'log_context_response',
        current_user,
        text,
        None
    )

    # only text for now
    log_entry = TextLogEntry.objects.get(id=payload["log_entry_id"])

    if "log_context_id" in payload:
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
    else:
        if text.strip().lower() != "none":
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
