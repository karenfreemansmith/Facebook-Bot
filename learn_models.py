import learn_db as db
import random


def update_count(table, id):
    value, count = db.find_row(table, id)
    count += 1
    db.update_data(table, id, value, count)


# *** CONTEXTS ***
def add_context(str, n):
    db.insert_data('contexts', str, n)
    return db.get_id('contexts', str)


def add_context_intent(context_id, intent_id):
    count = db.get_frequency('context_intents', context_id, intent_id)
    if count == 0:
        db.insert_relation('context_intents', context_id, intent_id)
    else:
        count += 1
        db.update_relation('context_intents', context_id, intent_id, count)


# *** INTENTS ***
def add_intent(str, n):
    db.insert_data('intents', str, n)
    return db.get_id('intents', str)


def add_intent_response(intent_id, response_id):
    count = db.get_frequency('intent_responses', intent_id, response_id)
    if count == 0:
        db.insert_relation('intent_responses', intent_id, response_id)
    else:
        count += 1
        db.update_relation('intent_responses', intent_id, response_id, count)


def add_intent_order(prompt, reply):
    prompt_id = db.get_id('intents', prompt)
    reply_id = db.get_id('intents', reply)
    db.insert_relation(prompt_id, reply_id)


# *** RESPONSES ***
def get_response(prompt_id):
    reply = 'let me think about that...'
    pr_ids = db.possible_ids('response_order',prompt_id)
    if len(pr_ids) > 0:
        reply, not_used = db.find_row('responses', random.choice(pr_ids))
    else:
        possible_responses = db.get_all('responses','score')
        reply = random.choice(possible_responses)[1]
    return reply


def add_response(trigger, str):
    id = db.get_id('responses', str)
    if id == 0:
        id = db.insert_data('responses', str, 1)
    else:
        update_count('responses',id)
    prompt_id = db.get_id('responses', trigger)
    db.insert_relation('response_order', prompt_id, id)
    i, c = add_tokens(id, str)
    add_intent_response(i, id)
    add_context_intent(c, i)
    return get_response(id)


# *** TOKENS ***
def add_response_token(response_id, token_id):
    count = db.get_frequency('response_tokens', response_id, token_id)
    if count == 0:
        db.insert_relation('response_tokens', response_id, token_id)
    else:
        count += 1
        db.update_relation('response_tokens', response_id, token_id, count)


def add_tokens(resp_id, str):
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter

    tokens = [w for w in word_tokenize(str.lower()) if w.isalpha()]
    no_stops = [t for t in tokens if t not in stopwords.words('english')]
    main_idea = Counter(no_stops).most_common(3)
    main_idea = [idea[0] for idea in main_idea]
    main_idea = sorted(main_idea)
    intent = '_'.join(main_idea)
    print("main idea? ", intent)

    tokens = word_tokenize(str.lower())
    for t in tokens:
        id = db.get_id('tokens', t)
        if id == 0:
            id = db.insert_data('tokens', t, 1)
        else:
            update_count('tokens',id)
        add_response_token(resp_id, id)

    #for t in tokens:
        # get token count
        # get sum of all token counts
        # % count/all_counts
        # max(t-score)
        # get intent/context * scores
    #return intent/context
    intent_id = 3
    context_id = 1
    return intent_id, context_id
