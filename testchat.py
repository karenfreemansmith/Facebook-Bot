import chat

msg = "hello"
while True:
    msg = input(chat.respond(msg) + "\n")
    if msg == 'goodbye':
        log = chat.get_log()
        for d in log:
            print(d)
        break
