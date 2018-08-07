import learn_models as m


def respond(bot_msg, human_msg):
    resp = m.add_response(bot_msg, human_msg)
    return resp
