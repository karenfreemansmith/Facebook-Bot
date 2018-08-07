import learn_models as m
import re


def respond(bot_msg, human_msg, sender):
    print('bot: ' + bot_msg)
    print(sender + ': ' + human_msg)
    resp = m.add_response(bot_msg, human_msg)
    resp = clean(resp)
    return resp


def clean(shit):
    stuff = re.compile("fuck|god|damn", re.I)
    cleaned = re.sub(stuff, "#@%$", shit)
    return cleaned
