import re
import random
import time

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey

engine = create_engine('sqlite:///chatter.db')

metadata = MetaData()

file = open('data/american_slave.txt', 'r')
t1 = file.read()
file.close()
#print(t1[0:59], len(t1))

file = open('data/alice_wonderland.txt', 'r')
t2 = file.read()
file.close()
#print(t2[0:59], len(t2))

file = open('data/anna_karenina.txt', 'r')
t3 = file.read()
file.close()
#print(t3[0:59], len(t3))

file = open('data/anne_avonlea.txt', 'r')
t4 = file.read()
file.close()
#print(t4[0:59], len(t4))

file = open('data/anne_green_gables.txt', 'r')
t5 = file.read()
file.close()
#print(t5[0:59], len(t5))

file = open('data/black_folk.txt', 'r')
t6 = file.read()
file.close()
#print(t6[0:59], len(t6))

file = open('data/call_wild.txt', 'r')
t7 = file.read()
file.close()
#print(t7[0:59], len(t7))

file = open('data/dracula.txt', 'r')
t8 = file.read()
file.close()
#print(t8[0:59], len(t8))

file = open('data/federalist_papers.txt', 'r')
t9 = file.read()
file.close()
#print(t9[0:59], len(t9))

file = open('data/frankenstein.txt', 'r')
t0 = file.read()
file.close()
#print(t0[0:59], len(t0))

t = t1+t2+t3+t4+t5+t6+t7+t8+t9+t0

file = open('data/grimm_fairytales.txt', 'r')
t1 = file.read()
file.close()
#print(t1[0:59], len(t1))

file = open('data/heart_darkness.txt', 'r')
t2 = file.read()
file.close()
#print(t2[0:59], len(t2))

file = open('data/iliad.txt', 'r')
t3 = file.read()
file.close()
#print(t3[0:59], len(t3))

file = open('data/little_women.txt', 'r')
t4 = file.read()
file.close()
#print(t4[0:59], len(t4))

file = open('data/moby_dick.txt', 'r')
t5 = file.read()
file.close()
#print(t5[0:59], len(t5))

file = open('data/outline_history.txt', 'r')
t6 = file.read()
file.close()
#print(t6[0:59], len(t6))

file = open('data/peter_pan.txt', 'r')
t7 = file.read()
file.close()
#print(t7[0:59], len(t7))

file = open('data/pinocchio.txt', 'r')
t8 = file.read()
file.close()
#print(t8[0:59], len(t8))

file = open('data/romance_lust.txt', 'r')
t9 = file.read()
file.close()
#print(t9[0:59], len(t9))

file = open('data/walden.txt', 'r')
t0 = file.read()
file.close()
#print(t0[0:59], len(t0))

t += t1+t2+t3+t4+t5+t6+t7+t8+t9+t0

file = open('data/pride_prejudice.txt', 'r')
t1 = file.read()
file.close()
#print(t1[0:59], len(t1))

file = open('data/sherlock_holmes.txt', 'r')
t2 = file.read()
file.close()
#print(t2[0:59], len(t2))

file = open('data/tom_sawyer.txt', 'r')
t3 = file.read()
file.close()
#print(t3[0:59], len(t3))

file = open('data/two_cities.txt', 'r')
t4 = file.read()
file.close()
#print(t4[0:59], len(t4))

file = open('data/war_peace.txt', 'r')
t5 = file.read()
file.close()
#print(t5[0:59], len(t5))

t += t1+t2+t3+t4+t5

t = t.replace(' "','')
t = t.replace('" ','')
t = t.replace('\n',' ')
t = t.replace('  ',' ')
t = t.replace('.','.\n')
t = t.replace(',',',\n')
t = t.replace(';',';\n')
t = t.replace('!','!\n')
t = t.replace('?','?\n')

t = t.split('\n')

r='?'

def ihasr(x):
    if r in x:
        #print(r, x.strip())
        return x.strip()

def respond(r):
    while r != 'quit':
        p = [x for x in t if ihasr(x) != None]
        print(len(p), 'choices')
        if len(p) > 0:
            resp = '\n' + random.choice(p) + '\n\n'
        else:
            resp = '\n' + random.choice(t) + '\n\n'
        time.sleep(len(resp)*0.01)
        r = input(resp)
        return r

def execute_query(query=''):
    if query == '' : return
    print (query)
    with engine.connect() as connection:
        try:
            connection.execute(query)
        except Exception as e:
            print(e)

def add_responses(phrase):
    query = "INSERT INTO responses(response, score) " \
            "VALUES ('{}','{}');".format(phrase, 1)
    execute_query(query)


def check_response(phrase):
    query = "SELECT count(score) FROM responses WHERE response == 'phrase';"
    execute_query(query)


for r in t:
    add_responses(r)
    check_response(r)
