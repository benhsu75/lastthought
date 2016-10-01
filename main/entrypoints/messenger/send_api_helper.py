import requests
from main.utils import constants

# Helper method to send different types of messages


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
    url_to_post = constants.FB_SEND_BASE_URL + constants.FB_PAGE_ACCESS_TOKEN
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
    url_to_post = constants.FB_SEND_BASE_URL + constants.FB_PAGE_ACCESS_TOKEN
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
    url_to_post = constants.FB_SEND_BASE_URL + constants.FB_PAGE_ACCESS_TOKEN
    r = requests.post(url_to_post, json=send_payload)


# Sends a message with account linking functionality
def send_account_link_message(fbid, text):
    send_payload = {
        'recipient': {
            'id': fbid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [{
                        'title': 'UserDataGraph Diary',
                        'image_url': '',
                        'buttons': [{
                            'type': 'account_link',
                            'url': 'https://userdatagraph.herokuapp.com/messenger_account_link',
                            "messenger_extensions": True
                        }]
                    }]
                }
            }
        }
    }
    url_to_post = constants.FB_SEND_BASE_URL + constants.FB_PAGE_ACCESS_TOKEN
    r = requests.post(url_to_post, json=send_payload)
    print r.text

def send_share_message(fbid, text):
    send_payload = {
        'recipient': {
            'id': fbid
        },
        'message': {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [{
                        'title': "Share LastThought",
                        'subtitle': text,
                        "item_url": constants.BASE_HEROKU_URL,
                        "image_url": "https://pbs.twimg.com/profile_images/675002642196729857/A0OpcJpA.png",
                        'buttons': [{
                            'type': 'element_share'
                        }]
                    }]
                }
            }
        }
    }
    url_to_post = constants.FB_SEND_BASE_URL + constants.FB_PAGE_ACCESS_TOKEN
    r = requests.post(url_to_post, json=send_payload)
    print r.text
