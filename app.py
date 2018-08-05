# import stuff as needed
from flask import Flask, request
import requests
import chat

app = Flask(__name__)
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'oh, this can be anything I want then?'
PAGE_ACCESS_TOKEN = 'EAAGs7tDg3NgBAIQRlRAZAY3Y15hfVznAMNRxZAjEiugaPyYuiU7q9rfi9U6DTrvoGhrpDT84t8aPaxamycVufOK3kFsjewKwBnntOCcrM07uMOy4gtxRNTB1Vs4JpmqdqdmwZC4ONZCrZBrsfXhVL7IwRxt7h9AVFSwWsoGRSjQZDZD'

# process messages
def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def send_message(sender, msg):
    text = chat.get_message(msg)

    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': sender
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


# listen for request
@app.route("/webhook", methods=['GET','POST'])
def listen():
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            text = x['message']['text']
            senderid = x['sender']['id']
            send_message(senderid, text)
        return "ok"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
