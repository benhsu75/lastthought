from main.message_log import message_log
from main.entrypoints.messenger import send_api_helper
from main.utils import helper_util, constants

# Helper method to send message for user to view logs
def send_view_logs_message(current_profile):
    # Send user message linking to log
    log_view_message = (
        "Click to view all your thoughts"
    )
    send_api_helper.send_button_message(current_profile.fbid, log_view_message, [
        {
            'type': 'web_url',
            'url': constants.BASE_HEROKU_URL,
            'title': 'View All'    
        }
    ])
    message_log.log_message(
        'log_view_message',
        current_profile,
        log_view_message,
        None
    )

# Helper method to send message to user to drill down into a specific category
def send_choose_category_message(current_profile):
    user_log = Log.find_or_create(current_profile)

    categories = LogContext.objects.filter(log=user_log)

    # Construct quick replies
    quick_replies = []
    count = 0
    for c in categories:
        count += 1

        count += 1

        if count <= 8:
            # Edit
            payload = json.dumps({
                "state": "view_specific_category",
                "category_id": c.id
            })
            quick_replies.append({
                "content_type": "text",
                "title": c.context_name,
                "payload": payload
            })

    # Actually send message
    choose_category_to_view_message = "...or choose a specific category to view your entries for:"
    send_api_helper.send_quick_reply_message(
        current_profile.fbid,
        choose_category_to_view_message,
        quick_replies
    )
    message_log.log_message(
        'log_add_context_message',
        current_profile,
        choose_category_to_view_message,
        None
    )


# Helper method to send message for user to view logs in specific category
def send_view_specific_category_message(current_profile, category):
    # Send user message linking to log
    log_view_message = (
        "Click to view your {} category".format(category.context_name)
    )
    link_to_view_category = '{}/categories/{}'.format(constants.BASE_HEROKU_URL, category.id)
    send_api_helper.send_button_message(current_profile.fbid, log_view_message, [
        {
            'type': 'web_url',
            'url': link_to_view_category,
            'title': 'View {}'.format(category.context_name)    
        }
    ])
    message_log.log_message(
        'log_view_message',
        current_profile,
        log_view_message,
        None
    )