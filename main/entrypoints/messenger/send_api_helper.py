import requests

# Helper method to send message
PAGE_ACCESS_TOKEN = 'EAADqZAUs43F4BAM24X91sSlhAIU7UHnLyO6eNp1rGMmQncyKsz34AgvlqfJKRnn3rNfYLMZBZA914L5z9MO8G6AVsGhljVUZCZAYtNfjbt0NKX7FFHDjOPvBcsiZCNzpSdNVZC4lCsbHVevRIhzKxFzjFzAMDVWq4W8KNuqtxXt8QZDZD'
SEND_BASE_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token='

# Send's a normal messenger text message
def send_basic_text_message(fbid, text):
    # Send message through FB Send API
    send_payload = {
        'recipient': {
            'id': fbid
        },
        'message': {
            'text': text
        }
    }
    url_to_post = SEND_BASE_URL + PAGE_ACCESS_TOKEN
    r = requests.post(url_to_post, json=send_payload)
    print(r.text)

# Sends a messenger text message with buttons
def send_button_message(fbid, text, button_list):
    # Send message through FB Send API
    send_payload = {
        'recipient': {
            'id': fbid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': text,
                    'buttons': button_list
                }
            }
        }
    }
    url_to_post = SEND_BASE_URL + PAGE_ACCESS_TOKEN
    r = requests.post(url_to_post, json=send_payload)
    print(r.text)

# Sends a message with quick replies (10 max)
def send_quick_reply_message(fbid, text, quick_replies):
    send_payload = {
        'recipient': {
            'id': fbid
        },
        'message': {
            'text': text,
            'quick_replies': quick_replies
        }
    }
    url_to_post = SEND_BASE_URL + PAGE_ACCESS_TOKEN
    r = requests.post(url_to_post, json=send_payload)
    print(r.text)
