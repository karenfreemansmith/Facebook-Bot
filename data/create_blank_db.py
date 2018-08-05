from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey

engine = create_engine('sqlite:///chatter.db')

metadata = MetaData()

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

response_order = Table('response_order', metadata,
                    Column('response_id', Integer),
                    Column('trigger_id', Integer),
                    Column('score', Integer))

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
