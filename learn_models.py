import learn_db as db
import random

def add_context(str, n):
    db.insert_data('contexts', str, n)
    return db.get_id('contexts', str)


def add_context_intent(context_id, intent_id):
    self.Intent.add_intent(str, n)
    db.insert_relation('context_intent', context_id, intent_id)
    return "ok"


def add_intent(str, n):
    db.insert_data('intents', str, n)
    return db.get_id('intents', str)


def add_intent_response(intent_id, response_id):
    db.insert_relation(intent_id, response_id)
    return "ok"


def add_intent_order(prompt, reply):
    prompt_id = db.get_id('intents', prompt)
    reply_id = db.get_id('intents', reply)
    db.insert_relation(prompt_id, reply_id)
    return "ok"


# RESPONSES
def get_response(prompt_id):
    reply = 'let me think about that...'
    pr_ids = db.possible_ids('response_order',prompt_id)
    if len(pr_ids) > 0:
        reply, not_used = db.find_row('responses', random.choice(pr_ids))
    else:
        possible_responses = db.get_all('responses','score')
        reply = random.choice(possible_responses)[1]
    return reply


def update_count(id):
    value, count = db.find_row('responses', id)
    count += 1
    db.update_data('responses', id, value, count)


def add_response(trigger, str):
    id = db.get_id('responses', str)
    if id == 0:
        id = db.insert_data('responses', str, 1)
    else:
        update_count(id)
    prompt_id = db.get_id('responses', trigger)
    db.insert_relation('response_order', prompt_id, id)
    return get_response(id)


def add_response_token(response_id, token_id):
    db.insert_relation(response_id, token_id)
    return "ok"


def add_token(str, n):
    db.insert_data('tokens', str, n)
    return db.get_id('tokens', str)
