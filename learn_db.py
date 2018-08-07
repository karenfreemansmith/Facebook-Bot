from sqlalchemy import create_engine
engine = create_engine('sqlite:///test.db')

def create_database():
    from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey
    metadata = MetaData()

    contexts = Table('contexts', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('score', Float))

    context_intents = Table('context_intents', metadata,
                        Column('parent_id', Integer, ForeignKey('contexts.id')),
                        Column('child_id', Integer, ForeignKey('intents.id')),
                        Column('frequency', Integer))

    intents = Table('intents', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('score', Float))

    intent_responses = Table('intent_responses', metadata,
                        Column('parent_id', Integer, ForeignKey('intents.id')),
                        Column('child_id', Integer, ForeignKey('responses.id')),
                        Column('frequency', Integer))

    responses = Table('responses', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
                        Column('score', Float))

    response_order = Table('response_order', metadata,
                        Column('parent_id', Integer, ForeignKey('responses.id')),
                        Column('child_id', Integer, ForeignKey('responses.id')),
                        Column('frequency', Integer))

    response_tokens = Table('response_tokens', metadata,
                        Column('parent_id', Integer, ForeignKey('responses.id')),
                        Column('child_id', Integer, ForeignKey('tokens.id')),
                        Column('frequency', Integer))

    tokens = Table('tokens', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('value', String),
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


def possible_ids(table, parent_id):
    query = "SELECT child_id FROM {} WHERE parent_id == {};".format(table,parent_id)
    results = []
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            print(e)
        else:
            for row in result:
                results.append(row[0])
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


def insert_data(table, str, n):
    query = '''INSERT INTO {}(value, score) VALUES ("{}",{});'''.format(table, str, n)
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            result = e
    return get_id(table, str)


def update_data(table, id, str, n):
    query = '''UPDATE {} SET value = '{}', score = {} WHERE id == {};'''.format(table, str, n, id)
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
        except Exception as e:
            result = e


def insert_relation(table, parent_id, child_id):
    query = '''INSERT INTO {}(parent_id, child_id, frequency) VALUES ({},{}, 1);'''.format(table, parent_id, child_id)
    with engine.connect() as connection:
        try:
            connection.execute(query)
        except Exception as e:
            print(e)


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
