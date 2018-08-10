from sqlalchemy import create_engine
engine = create_engine('sqlite:///copy.db')
copy_engine = create_engine('sqlite:///chat.db')
#engine = create_engine('sqlite:///test.db')

def run_query(query):
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            print(e)


def copy_all(table,start,stop,prompt):

    query = "SELECT * FROM {} WHERE id > {} AND id < {}".format(table, start, stop)
    results = []
    with copy_engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            print(e)
        else:
            import learn_models as m
            for row in result:
                print(row)
                m.add_response(prompt,row.value)
            result.close()


def view_all(r):
    query = "SELECT c.value, i.value, r.id, r.value FROM contexts AS c \
            JOIN context_intents AS ci\
            ON c.id == ci.parent_id \
            JOIN intents AS i \
            ON ci.child_id == i.id \
            JOIN intent_responses AS ir\
            ON i.id == ir.parent_id \
            JOIN responses AS r \
            ON ir.child_id == r.id \
            WHERE r.id = {};".format(r)
    results = []

    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            print(e)
        else:
            for row in result:
                print(row)
            result.close()


def create_database():
    from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey
    metadata = MetaData()

    users = Table('users', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('details', String),
                        Column('count', Integer),
                        Column('score', Float))

    contexts = Table('contexts', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('details', String),
                        Column('count', Integer),
                        Column('score', Float))

    context_intents = Table('context_intents', metadata,
                        Column('parent_id', Integer, ForeignKey('contexts.id')),
                        Column('child_id', Integer, ForeignKey('intents.id')),
                        Column('frequency', Integer))

    intents = Table('intents', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('details', String),
                        Column('count', Integer),
                        Column('score', Float))

    response_order = Table('intent_order', metadata,
                        Column('parent_id', Integer, ForeignKey('intents.id')),
                        Column('child_id', Integer, ForeignKey('intents.id')),
                        Column('frequency', Integer))

    intent_responses = Table('intent_responses', metadata,
                        Column('parent_id', Integer, ForeignKey('intents.id')),
                        Column('child_id', Integer, ForeignKey('responses.id')),
                        Column('frequency', Integer))

    responses = Table('responses', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('details', String),
                        Column('count', Integer),
                        Column('score', Float))

    response_order = Table('response_order', metadata,
                        Column('parent_id', Integer, ForeignKey('responses.id')),
                        Column('child_id', Integer, ForeignKey('responses.id')),
                        Column('frequency', Integer))

    response_tokens = Table('response_tokens', metadata,
                        Column('parent_id', Integer, ForeignKey('intents.id')),
                        Column('child_id', Integer, ForeignKey('tokens.id')),
                        Column('frequency', Integer))

    tokens = Table('tokens', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('details', String),
                        Column('count', Integer),
                        Column('score', Float))

    try:
        metadata.create_all(engine)
        print("Tables created")
    except Exception as e:
        print("Error occurred during Table creation!")
        print(e)


def print_all(table, condition):
    query = "SELECT * FROM {} ORDER BY {};".format(table,condition)
    results = []
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            print(e)
        else:
            for row in result:
                print(row)
            result.close()


def show_context_intent_reponses(c,i):
        query = "SELECT c.value, i.value, r.id, r.value FROM contexts AS c \
                JOIN context_intents AS ci\
                ON c.id == ci.parent_id \
                JOIN intents AS i \
                ON ci.child_id == i.id \
                JOIN intent_responses AS ir\
                ON i.id == ir.parent_id \
                JOIN responses AS r \
                ON ir.child_id == r.id \
                WHERE c.id = {} AND i.id = {};".format(c, i)
        results = []
        with engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)
                result.close()


def get_all(table, condition):
    query = "SELECT * FROM {} ORDER BY {};".format(table,condition)
    results = []
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            print(e)
        else:
            for row in result:
                results.append(row)
            result.close()
    return results


def possible_ids(c,i):
    if False:
        print(find_row('contexts',c))
        print(find_row('intents',i))
    else:
        query = "SELECT c.value, i.value, r.id, r.value FROM contexts AS c \
                JOIN context_intents AS ci\
                ON c.id == ci.parent_id \
                JOIN intents AS i \
                ON ci.child_id == i.id \
                JOIN intent_responses AS ir\
                ON i.id == ir.parent_id \
                JOIN responses AS r \
                ON ir.child_id == r.id \
                WHERE c.id = {} AND i.id = {};".format(c, i)
        results = []
        with engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    results.append(row[2])
                result.close()
        return results


def find_row(table, id):
    query = "SELECT value, score FROM {} WHERE id = {};".format(table,id)
    value, count = '', 0
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
            for row in result:
                value = row[0]
                count = row[1]
        except Exception as e:
            print(e)
        else:
            result.close()
    return value, count


def insert_data(table, label, n):
    query = '''INSERT INTO {}(value, score) VALUES ("{}",{});'''.format(table, label, n)
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            result = e
    return get_id(table, label)


def update_data(table, id, str, n):
    query = '''UPDATE {} SET value = "{}", score = {} WHERE id == {};'''.format(table, str, n, id)
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            result = e


def get_frequency(table, parent_id, child_id):
    query = '''SELECT frequency FROM {} WHERE parent_id == {} AND child_id == {};'''.format(table, parent_id, child_id)
    count = 0
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
            for row in result:
                count = row[0]
                print('updated count: ', count)
        except Exception as e:
            print(e)
        else:
            result.close()
    return count


def insert_relation(table, parent_id, child_id):
    query = '''INSERT INTO {}(parent_id, child_id, frequency) VALUES ({},{}, 1);'''.format(table, parent_id, child_id)
    with engine.connect() as connection:
        try:
            connection.execute(query)
        except Exception as e:
            print(e)


def update_relation(table, parent_id, child_id, frequency):
    query = '''UPDATE {} SET frequency = '{}' WHERE parent_id == {} AND child_id == {};'''.format(table, frequency, parent_id, child_id)
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            result = e


def get_id(table, value):
    query = '''SELECT id FROM {} WHERE value = "{}";'''.format(table, value)
    id = 0
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
            for row in result:
                id=row[0]
        except Exception as e:
            print(e)
        else:
            result.close()
    return id
