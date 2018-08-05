from sqlalchemy import create_engine
engine = create_engine('sqlite:///chatter.db')

def execute_query(query):
    responses = []
    with engine.connect() as connection:
        try:
            result = connection.execute(query)
            for row in result:
                responses.append(row[0])
        except Exception as e:
            #print (query)
            #print(e) #getting a lot that don't return results, may need another option for executing insert/updates
            responses = []
    return responses


def default_responses(prompt):
    query = "SELECT response FROM responses ORDER BY score"
    result = execute_query(query)
    responses = result

    return responses


def add_response(phrase):
    query = "INSERT INTO responses(response, score) VALUES ('''{}''','{}');".format(phrase, 1)
    execute_query(query)


def check_response(phrase, msg):
    query = "SELECT id FROM responses WHERE response=='''{}''' ORDER BY score".format(phrase)
    results = execute_query(query)
    if len(results) > 0:
        response_id = results[0]
        score = execute_query("SELECT score FROM responses WHERE id = {}".format(response_id))
        new_score = score[0]+1.0
        query = "UPDATE responses set score={} WHERE id={}".format(new_score,response_id)
        execute_query(query)
    else:
        add_response(phrase)
    #update_order(phrase, msg)


def update_order(response, trigger):
    r_id = get_id(response)
    t_id = get_id(trigger)
    s = check_existing(r_id, t_id)
    query = "UPDATE response_order set score={} WHERE response_id = {} AND trigger_id = {}".format(s,r_id, t_id)
    execute_query(query)


def get_id(r):
    query = "SELECT id FROM responses WHERE response=='{}' ORDER BY score".format(r)
    results = execute_query(query)
    response_id = 0
    if len(results) > 0:
        response_id = results[0]
    return response_id


def check_existing(r_id, t_id):
    query = "SELECT score FROM response_order WHERE response_id = {} AND trigger_id = {}".format(r_id, t_id)
    score = execute_query(query)
    if score == None:
        query = "INSERT INTO response_order(response_id, trigger_id, score) VALUES ('{}','{}','{}');".format(r_id, t_id, 1)
        score = 1
    else:
        if len(score) > 0:
            score = execute_query(query)
            score = score[0] + 1
    return score


def get_emoji():
    emojis = ["LOL","😉","💩","😭","😃","😊",'😇','😘','😇','😏','😳',
        '😍','👽',"😅",'😱','😫','😬','😈','👿','😡','😤','😖',
        '😎','😋','😴','😒','👏','👍','👀', "👻",'🔥','💰','☕',
        '🍭','🍩',"🐾",'🍄','🌹',"🌺",'OMG',"Oh, wow...",'Okay',
        'I hope so!','Tell me more...','I feel the same.','TMI']
    return random.choice(emojis)
