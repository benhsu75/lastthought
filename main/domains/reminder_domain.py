from main.entrypoints.messenger import send_api_helper


def send_reminder_message(fbid):
    reminder_message = "Let's get your diary started with a selfie! Tap the camera below this message, and send me a selfie :)"
    send_api_helper.send_basic_text_message(
        current_profile.fbid,
        reminder_message
    )
    message_log.log_message(
        'reminder_message',
        current_profile,
        reminder_message,
        None
    )
