from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.models import *
from main.utils import helper_util

BASE_HEROKU_URL = 'http://userdatagraph.herokuapp.com'


def handle_log_entry(current_user, text, processed_text):
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

        log_contexts = LogContext.objects.filter(log=user_log)

        quick_replies = []
        for context in log_contexts:
            quick_replies.append({
                "content_type": "text",
                "title": context.context_name,
                "payload": "LOG_CONTEXT-" + context.id
            })

        quick_replies.append({
            "content_type": "text",
            "title": "Add a new context",
            "payload": "LOG_CONTEXT-NEW"
        })

        send_api_helper.send_quick_reply_message(
            current_user.fbid,
            "Add a context to your log entry?",
            quick_replies
        )
