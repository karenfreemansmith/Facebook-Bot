import learn_db as db


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
    value, count = db.find_row('responses', prompt_id)
    return value


def update_count(id):
    value, count = db.find_row('responses', id)
    count += 1
    db.update_data('responses', id, value, count)


def add_response(str):
    id = db.get_id('responses', str)
    if id == 0:
        db.insert_data('responses', str, 1)
    else:
        update_count(id)
    return get_response(db.get_id('responses', str))


def add_response_token(response_id, token_id):
    db.insert_relation(response_id, token_id)
    return "ok"


def add_token(str, n):
    db.insert_data('tokens', str, n)
    return db.get_id('tokens', str)
