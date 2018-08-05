import time
import re
import random
import chat_responses as chat



# process incoming message:
thisChat = []
prev_bot_text = 'Hello. :)'
def get_message(msg):
    text = prev_bot_text
    # add message to database of responses (or increment count if it is already there)
    chat.check_response(msg, prev_bot_text)
    thisChat.append('human: ' + msg)

    # check rules to see if there is a response format
    # check to see if intent is recognized

    # look for default responses
    if len(chat.default_responses(msg)) > 0:
        text = random.choice(chat.default_responses(msg))
#    if text=='.':
#        random.choice(chat.get_emoji())
    return text

# return message
def respond(msg):
    text = get_message(msg)
    thisChat.append('bot:' + text)
    prev_bot_text = text

    time.sleep(len(text)*0.01)
    return text


def get_log():
    return thisChat
