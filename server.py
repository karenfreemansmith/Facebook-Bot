from flask import Flask, request

import requests

import chitchat

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'oh, this can be anything I want then?'
PAGE_ACCESS_TOKEN = 'EAAGs7tDg3NgBAIQRlRAZAY3Y15hfVznAMNRxZAjEiugaPyYuiU7q9rfi9U6DTrvoGhrpDT84t8aPaxamycVufOK3kFsjewKwBnntOCcrM07uMOy4gtxRNTB1Vs4JpmqdqdmwZC4ONZCrZBrsfXhVL7IwRxt7h9AVFSwWsoGRSjQZDZD'


def get_bot_response(message):
    """This is just a placeholder where some real nlp stuff will eventually go when the app is developed beyond the tutorial level"""
    return chitchat.send_message(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def respond(sender, message):
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    return (message.get('message') and message['mesasge'].get("is_echo"))


@app.route("/webhook", methods=['GET','POST'])
def listen():
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            text = x['message']['text']
            sender_id = x['sender']['id']
            respond(sender_id, text)
        return "ok"


def send_message(recipient_id, text):
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post (
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
