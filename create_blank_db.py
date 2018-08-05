import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey

engine = create_engine('sqlite:///chatter.db')

metadata = MetaData()

'''
Within this database I should have tables for:
- contexts
- intents
- responses
- words/tokens
as well as tables that join these things in many-to-many relationships

I want to be able to analyze a response and put it into the appropriate place(s) in the database whenever anyone interacts with my bot. I should be able to start from one response (a smiley face, or the word 'hi') and then build out a fully conversational model for my bot based on the interactions it has with the outside world.

For "morals" I want to assign a vector to each response (or token? or intent?) as to how "acceptable" it is in a given context...positive or negative... and so from -5 thru 0 thru +5 and then give each interaction a weight that will nudge the scale.

As humans we have weights like "god", "parents", "teachers", "friends", and "enemies" that may get positive or negative nudges for various topics. I want to emulate that system somehow. I want people to have to earn trust in order to influence my bot. Everyone will not be treated equally (well, perhaps at first...)


Sentence builder (probably another module, but this is just some late night notes here, so more structure in the morning, right?)

I want to be able to read and write sentences with some intention or understanding... ie subject verb predicate... to identify who did what to whom and respond correctly in many forms of the sentence.

I want to correctly identify adjectives/adverbs and if they are positive or negative, when they are opposite in meaning (quick/slow, big/small), so there should be some kind of "picker" functions for each part of speech. Initially the sentences may be nonsense, but they shoudl be real sentences (and this also applies to my typing website - which has some primitive forms of it and could benefit from more advanced forms.)

I could totally add chatbots to my websites for Aspiring Writers (a "muse bot", and a good idea for an app as well. Tell it about your story and when you get stuck it will offer suggestions for the next plot twist) and for World Langauge Library as the language pages could benefit from a very controlled bot that can converse with you in the target language to practice your current lessons/progress through the languages. Again, a good place for an app as well as on the web-pages.

And finally, while thinking about my website empire... there are so many topics I could explore as blog posts/pages on my machine learning website. All the notes from the ML conference, and my notebooks from DataCamp and the books I'm reading. Every chapter is worth at least one blog post once it's broken down and reworded.  And if I take the time to get creative on my angle it may even be somehting really compelling in terms of the space online.

I think I need to focus more on this than on the job search for the time being. I do not think my current job hunt is going all that well, lots of bites, but lots of fish I don't want to take home and fry up for dinner if that makes sense.
'''

contexts = Table('contexts', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('context', String),
                    Column('score', Float))

context_intents = Table('context_intents', metadata,
                    Column('context_id', Integer, ForeignKey('contexts.id')),
                    Column('intent_id', Integer, ForeignKey('intents.id')),
                    Column('score', Float))

intents = Table('intents', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('intent', String),
                    Column('score', Float))

intent_responses = Table('intent_responses', metadata,
                    Column('intent_id', Integer, ForeignKey('intents.id')),
                    Column('response_id', Integer, ForeignKey('responses.id')),
                    Column('score', Float))

responses = Table('responses', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('response', String),
                    Column('score', Float))

response_tokens = Table('response_tokens', metadata,
                    Column('response_id', Integer, ForeignKey('responses.id')),
                    Column('token_id', Integer, ForeignKey('tokens.id')),
                    Column('score', Float))

tokens = Table('tokens', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('token', String),
                    Column('score', Float))


try:
    metadata.create_all(engine)
    print("Tables created")
except Exception as e:
    print("Error occurred during Table creation!")
    print(e)
