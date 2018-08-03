import chitchat

msg = "hello"
while True:
    msg = input(chitchat.send_message(msg) + "\n")
    if msg == 'goodbye':
        break
