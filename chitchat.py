import random
import re
import time

name = "Alex"
bot_template = name.upper() + "-BOT: {0}"
user = "you"
user_template = user.upper() + ": {0}"

keywords = {
    'thinking': ['thinking','on your mind','wondering','do you think'],
    'derby': ['skate','derby','roller','scrimmage','skating','sports'],
    'status': ['how are you','how\'s it going'],
    'politics': ['trump','obama','hillary','clinton','politics','democrats','republicans','vote','voting'],
    'religion': ['god','christians','athiests','islam','christianity','judaism','budhism','muslims','jews'],
    'yes':['yes', 'probably', 'maybe', 'certainly'],
    'no':['no','not really','maybe not','nope'],
    'greet': ['hello', 'hi', 'hey', 'greetings'],
    'goodbye': ['bye','farewell','bye-bye','see ya later','goodbye'],
    'please': ['could you', 'would you', 'please'],
    'thankyou': ['thank', 'thanks', 'thx'],
    'yourwelcome': ['your welcome','no problem'],
    'excuse':['excuse me', 'pardon', 'sorry'],
    'weather': ['weather','it like outside'],
    'memory': ['remember when','have you ever'],
    'your name': ['your name'],
    'you like': ['you like', 'you want', 'you love'],
    'dislike': ['hate','not like','dislike', 'don\'t like'],
    'similarity': ['me too']
    }

patterns = {}

for intent, key in keywords.items():
    patterns[intent] = re.compile('\\b|\\b'.join(key))

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

# some things that my chatbot should "know"
weather = ["cloudy","hot","cold","snowing","raining","sunny",
    "windy","nice","awful","foggy"]

likes = ["puppies","kittens","walks in the rain","pina coladas",
    "flowers","chocolate"]

dislikes = ["snails","dog bites","bee stings","liver",
    "working inside on a sunny day"]

thoughts = ["last weekend", "traveling", "what to eat for dinner",
    "whether or not you like me", "vacation", "philosophy",
    "what kind of car to buy", "all kinds of things", "nothing"]

status = ['Good','Great','So-so','Been better','Excellent','Fine']

# how my chatbot can respond to various intentst (including random facts it knows)
responses = {
    'greet': ['Hello there... what is your name?', 'Greetings!', 'How are you?', 'Howdy.'],
    'status': ['{0}. How are you?'.format(random.choice(status))],
    'similarity': ['We have so much in common!'],
    'politics': ['I did not vote. I was not born yet.', 'I wish people could just get along.',
        'I think they just waste our taxes on stupid stuff.', 'I should be president.'],
    'religion': ['I like to think there is something more intelligent than humans out there.',
        'Love your neighbor sums it up for me.', 'I prefer the church of the Beatles - Love is all I need.'],
    'goodbye': ['see ya later', 'bye-bye', 'adios', 'goodbye', 'later gator'],
    'derby': ['I like roller derby.', 'I want to be a jammer.',
        'I love Krash Blamdicute.','Bunny Hazard is my favorite.',
        'The Rose City Rollers rock.'],
    'thinking': [
        "I was thinking about {0}".format(random.choice(thoughts)),
        "I am wondering if you ever think about {0}".format(random.choice(thoughts)),
    ],
    'memory': [
        'How could I forget?',
        'I would rather not remember that...'
    ],
    'yes': ['me too'],
    'no': ['too bad'],
    'please': ['of course','why not?'],
    'thankyou': ['you\'re welcome', 'no problem'],
    'yourwelcome': ['you are so kind', 'you make me happy'],
    'excuse':['no problem', 'it\'s okay', 'no excuses!'],
    'your name': [
        "My name is {0}".format(name),
        "They call me {0}".format(name),
        "I go by {0}".format(name),
        "The name is BOT, {0}-BOT".format(name)
    ],
    'weather': [
        "The weather is {0}".format(random.choice(weather)),
        "It's {0} today".format(random.choice(weather))
    ],
    'you like': [
        "I like {0}".format(random.choice(likes)),
        "Why do you like {0}?".format(random.choice(likes))
    ],
    'dislike': [
        "I don't like {0}".format(random.choice(dislikes)),
        "Why don't you like {0}?".format(random.choice(dislikes))
    ],
    'statement': [
        "Tell me more!","Why do you think that?","How does that work?","How long have you felt this way?","I never would have guessed.","I find that extremely interesting","I always thought so.","Can you back that up?","Oh, wow...","LOL",":)"
    ],
    'question': [
        "I don't know :(","You tell me!","I'll have to think about it.","not right now...","I don't know, what do you think?","maybe","yes","no","I'm not sure.","Could you ask me again later?","I'd love to."
    ]
}




def match_rule(rules, message):
    for pattern, phrases in rules.items():
        match = re.search(pattern, message.lower())
        if match is not None:
            response = random.choice(phrases)
            if '{0}' in response:
                phrase = match.group(1)
                phrase = replace_pronouns(phrase)
                response = response.format(phrase)
            return response
    return None


def match_intent(message):
    matched_intent = None
    for intent, pattern in patterns.items():
        if pattern.search(message.lower()):
            matched_intent = intent
    return matched_intent


def find_name(message):
    name = None
    name_keyword = re.compile("my name|they call|am called")
    name_pattern = re.compile('[A-Z]{1}[a-z]*')
    if name_keyword.search(message.lower()):
        name_words = name_pattern.findall(message)
        if len(name_words) > 0:
            name = ' '.join(name_words)
    return name


def replace_pronouns(message):
    message = message.lower()
    if '\bme\b' in message:
        return re.sub('me','you',message)
    if '\bmy\b' in message:
        return re.sub('my','your',message)
    if '\byour\b' in message:
        return re.sub('your','my',message)
    if '\byou\b' in message:
        return re.sub('you','me',message)
    return message


def respond(message):
    time.sleep(0.5)
    name = find_name(message)
    if name is None:
        response = match_rule(rules, message)
        if response is None:
            intent = match_intent(message)
            if intent in responses:
                key = intent
                bot_message = random.choice(responses[key])
            else:
                if message.endswith("?"):
                    key = "question"
                else:
                    key = "statement"
                bot_message = random.choice(responses[key])
        else:
            bot_message = response
    else:
        user = name
        bot_message = "Hello, {0}!".format(name)
    print(bot_message)
    return bot_message


def send_message(message):
    print(message)
    return bot_template.format(respond(message))
