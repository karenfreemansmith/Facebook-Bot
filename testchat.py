import learn_chat as chat

bot_msg = "Hello! :)"
h_reply = input("BOT: " + bot_msg + "\n")

while True:
    bot_msg = chat.respond(bot_msg, h_reply, 'the creator')
    h_reply = input("BOT: " +  bot_msg + "\n")
    if h_reply == 'quit':
        break
