import learn_chat as chat

bot_msg = "Hello! :)"
h_reply = input("BOT: " + bot_msg + "\n")

while True:
    bot_msg = chat.respond(bot_msg, h_reply)
    h_reply = input("BOT: " +  bot_msg + "\n")
    if h_reply == 'q':
        #log = chat.get_log()
        #for d in log:
            #print(d)
        break
