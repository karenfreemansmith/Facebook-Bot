import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey

engine = create_engine('sqlite:///chatter.db')

metadata = MetaData()

'''

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

responses = Table('response_order', metadata,
                    Column('prompt_id', Integer, ForeignKey('responses')),
                    Column('reply_id', Integer, ForeignKey('responses')),
                    Column('frequency', Integer))

response_tokens = Table('response_tokens', metadata,
                    Column('response_id', Integer, ForeignKey('responses.id')),
                    Column('token_id', Integer, ForeignKey('tokens.id')),
                    Column('score', Float))

tokens = Table('tokens', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('token', String),
                    Column('score', Float))

#try:
#    metadata.create_all(engine)
#    print("Tables created")
#except Exception as e:
#    print("Error occurred during Table creation!")
#    print(e)


import nltk
#from nltk.book import *

def print_all_data(table='', query=''):
    query = query if query != '' else "SELECT * FROM '{}' ORDER BY score;".format(table)
    print(query)
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            print(e)
        else:
            for row in result:
                print(row) # print(row[0], row[1], row[2])
            result.close()
    print("\n")

def execute_query(query=''):
    if query == '' : return
    print (query)
    with engine.connect() as connection:
        try:
            connection.execute(query)
        except Exception as e:
            print(e)


def add_tokens(word, s):
    query = "INSERT INTO tokens(token, score) " \
            "VALUES ('{}','{}');".format(word, s)
    execute_query(query)


#import Pandas as pd
#import numpy as np

def collect_tokens():
    text1_wordlist = list(sorted(text1))
    text2_wordlist = list(sorted(text2))
    text3_wordlist = list(sorted(text3))
    text4_wordlist = list(sorted(text4))
    text5_wordlist = list(sorted(text5))
    text6_wordlist = list(sorted(text6))
    text7_wordlist = list(sorted(text7))
    text8_wordlist = list(sorted(text8))
    text9_wordlist = list(sorted(text9))
    wordlist = text1_wordlist + text2_wordlist + text3_wordlist + text4_wordlist + text5_wordlist + text6_wordlist + text7_wordlist + text8_wordlist + text9_wordlist
    wordlist = [w.lower() for w in wordlist]
    all_words = list(sorted(set([w for w in wordlist if w.isalpha()])))
    print(len(all_words), 'words')
    scores = []
    for w in all_words:
        s = (100000.0 * wordlist.count(w))/(1.0 * len(wordlist))
        print(w,s)
        scores.append(s)
        add_tokens(w, s)
    words_df = pd.DataFrame({'word':all_words, 'score':scores})
    pd.to_csv('allwords.csv')
    print(words_df.head())


print_all_data('tokens')

#collect_tokens()
