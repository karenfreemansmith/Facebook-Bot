import spacy

nlp = spacy.load('en')
nlp.vocab.vectors_length

def respond(message):
    doc = nlp(message)

    for token in doc:
        print("{} : {}".format(token, token.vector[:3]))

msg = ""

while msg != "bye":
    msg = input("enter a phrase: ")
    print(respond(msg))
