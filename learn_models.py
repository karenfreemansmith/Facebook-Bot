import learn_db as db
import random
import re

bot = {
    "name":"Alex"
}

user = {
    "name":"you"
}

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
def get_response(prompt_id, c, i):
    if False:
        reply = 'let me think about that...'
    else:
        pr_ids = db.possible_ids(c,i)
        if len(pr_ids) > 0:
            reply, not_used = db.find_row('responses', random.choice(pr_ids))
        else:
            possible_responses = db.get_all('responses','score')
            reply = "no response found" #random.choice(possible_responses)[1]
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
    return get_response(id, c, i)


# *** TOKENS ***
def add_response_token(response_id, token_id):
    count = db.get_frequency('response_tokens', response_id, token_id)
    if count == 0:
        db.insert_relation('response_tokens', response_id, token_id)
    else:
        count += 1
        db.update_relation('response_tokens', response_id, token_id, count)


def add_tokens(resp_id, str):
    #manage_tokens(resp_id, str)
    return analyze_context_intent(resp_id)


def analyze_context_intent(resp_id):
    str, n = db.find_row('responses', resp_id)
    print(str)
    return find_intent(str), find_context(str)


def manage_tokens(resp_id, str):

    # some things that my chatbot should "know"
    # these wordlists seem a lot like I am thining the tokens
    # may actually need to relate to context or intent than
    # pointing back to the responses they came from...
    weather = ["cloudy","hot","cold","snowing","raining","sunny",
        "windy","nice","awful","foggy"]

    likes = ["kittens","walks in the rain","pina coladas",
        "flowers","puppies","chocolate"]

    dislikes = ["snails","dog bites","bee stings","liver",
        "working inside on a sunny day"]

    thoughts = ["last weekend", "traveling", "what to eat for dinner",
        "whether or not you like me", "vacation", "philosophy",
        "what kind of car to buy", "all kinds of things", "nothing"]

    status = ['Good','Great','So-so','Been better','Excellent','Fine']
    # and at some point the bot should be able to ask about a
    # new token and verify that it belongs to a certain context/intent
    # possibly when multiple users agree that it does.

    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter

    tokens = word_tokenize(str.lower())
    for t in tokens:
        id = db.get_id('tokens', t)
        if id == 0:
            id = db.insert_data('tokens', t, 1)
        else:
            update_count('tokens',id)
        add_response_token(resp_id, id)
    print(tokens)

    tokens = [w for w in word_tokenize(str.lower()) if w.isalpha()]
    no_stops = [t for t in tokens if t not in stopwords.words('english')]
    main_idea = Counter(no_stops).most_common(3)
    main_idea = [idea[0] for idea in main_idea]
    main_idea = sorted(main_idea)
    intent = '_'.join(main_idea)
    print("main idea? ", intent)

    # is this done already?
    #for t in tokens:
        # get token count
        # get sum of all token counts
        # % count/all_counts
        # max(t-score)
        # get intent/context * scores
    #return intent/context

    # ALSO TODO: need to revise/reverse tables for intents and context (and the patched code...)
    # TODO: test this in a container - run bin/bash and testchat.py so that the test does not
    # alter the base database that is started.
    # TODO: might also be good to transfer from this chat.db to a new one and create fresh
    # relationships for the various responses (but not have to type them all again if possible)
    # and if that works... then the test.db might be good to try and transfer as well???

    # and do I need these tokens? is there a purpose for having this here? will I evern use it, or
    # will I find some rules-based way to collect new intents?


def find_intent(str):
    # I think that the idea behind these keywords is pretty much
    # the same as "intent" - so maybe i can reuse this logic in
    # some way to simplify the if/then stuff below?
    intents = {
        '1' :['hello','hi','your name','favorite','how old','how are you'],
        '2' :['food','drink','alcohol','beer','meat','vegetable','fruit','dairy','grains','vegetarian', 'vegan','restaurant','eat'],
        '3' :['music','song','instument','country','rock','classical','folk','concert'],
        '4' :['movies','theater','drama','comedy','action','romance','film'],
        '5' :['actor','actress','musician','politician','author'],
        '6' :['tv','show'],
        '7' :['hobbies','interest','pastime','for fun'],
        '8' :['game','role playing games','card games','cards','dice','board games'],
        '9' :['animal','pet','dog','cat','bunny','snake','rat','dragon'],
        '10':['sports','roller derby','fishing','boxing','football','basketball','running'],
        '11':['art','painting','drawing','sculpture','crafts'],
        '12':['fashion', 'shoes', 'clothes', 'tattoo', 'piercing', 'hair', 'color'],
        '13':['technology', 'app', 'internet', 'phone', 'computer'],
        '14':['annoy','bother'],
        '15':['personality','introvert','extrovert','shy','outgoing'],
        '16':['ability','skill','talent'],
        '17':['goals','retire'],
        '18':['success'],
        '19':['work', 'job', 'a living'],
        '20':['friend','boss','co-worker','neighbor','rival'],
        '21':['book','magazine','fiction','non-fiction','novel','story'],
        '22':['weekend','vacation'],
        '23':['travel','vacation','world','go to another'],
        '24':['season','holiday','christmas','easter','halloween','new year'],
        '25':['family','parent','kid','brother','sister','aunt','uncle'],
        '26':['school', 'college', 'course'],
        '27':['childhood'],
        '28':['life','meaning','philosophy'],
        '29':['if','imagine'],
        '30':['education','school board','standardized tests','teachers'],
        '31':['politics','vote','democrat','republican','president','trump','clinton','hillary','obama'],
        '32':['religion','god','christian','islam','infidel','athiest','agnostic','catholic','protestant', 'muslim','jew','buddhist','jesus','christ','mohamed','budha','confucious'],
        '33':['lifestyle','vegan','lgbtq'],
        '34':['dating','have a boyfriend','have a girlfriend','on a date','want to go out'],
        '35':['sex','fuck','cunt','cock','cum','foreplay'],
        '36':['unknown']}

    patterns = {}
    for intent, key in intents.items():
        patterns[intent] = re.compile('\\b|\\b'.join(key))

    matched_intent = '36'
    for intent, pattern in patterns.items():
        if pattern.search(str.lower()):
            matched_intent = intent
    return int(matched_intent)


def find_context(str):
    # I think that the idea behind these rules is pretty much
    # the same as "context" - so maybe i can reuse this logic in
    # some way to simplify the if/then stuff below?
    rules = {
        'do you speak (.*)':[
            'Of course I speak {0}',
            'No. I do not speak {0}',
            ],
        'do you understand (.*)':[
            'Of course I understand {0}',
            'No. I do not understand {0}',
            ],
        'do you like (.*)':[
            'Of course I like {0}',
            'Oh, I love {0}',
            "I'm not so fond of {0}",
            "No. I don't like {0}",
            ],
        'do you remember (.*)': [
            'Did you think I would forget {0}',
            "Why haven't you been able to forget {0}",
            'What about {0}', 'Yes .. and?'
            ],
        'if (.*)': [
            "Do you really think it's likely that {0}",
            'Do you wish that {0}',
            'What do you think about {0}',
            'Really--if {0}'
            ],
        'do you think (.*)': [
            'if {0}? Absolutely.',
            'you would not believe how often I think {0}',
            '{0}? never...'
            ],
        'i want (.*)': [
            'What would it mean to you if you got {0}',
            'Why do you want {0}',
            "What's stopping you from getting {0}",
            'I want {0} too.'
            ]
        }

    #for pattern, phrases in rules.items():
    #    match = re.search(pattern, message.lower())
    #    if match is not None:
    #        response = random.choice(phrases)
    #        if '{0}' in response:
    #            phrase = match.group(1)
    #            phrase = replace_pronouns(phrase)
    #            response = response.format(phrase)
    #        return response
    #return None

    contexts = {
        '1':['talk about','chat about'],
        '2':['heard','read','saw'],
        '3':['if','imagine'],
        '4':['who','what','when','where','how','why'],
        '5':['yes','agree','go on','tell me more'],
        '6':['think','believe','feel'],
        '7':['not talk about','bored']}

    patterns = {}
    for context, key in contexts.items():
        patterns[context] = re.compile('\\b|\\b'.join(key))

    matched_context = '2'
    for context, pattern in patterns.items():
        if pattern.search(str.lower()):
            matched_context = context
    return int(matched_context)
