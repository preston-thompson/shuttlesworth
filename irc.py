import socket

sock = None
buf = str()

def send(s):
    print("send: " + s)
    sock.send(bytes(s) + b"\r\n")

def receive():
    global buf
    while "\r\n" not in buf:
        text = sock.recv(1024).decode("utf-8")
        buf += text
    rv = buf[:buf.index("\r\n")]
    buf = buf[buf.index("\r\n") + 2:]
    print("recv: " + rv)
    return rv

def connect(server, port, nick):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    while "NOTICE Auth :" not in receive():
        pass
    send("USER %s %s %s :%s\r\n" % (nick, nick, nick, nick))
    send("NICK %s\r\n" % nick)
    while "NOTICE Auth :Welcome" not in receive():
        pass

def join(channel):
    send("JOIN %s" % channel)

def privmsg(recipient, message):
    send("PRIVMSG %s :%s" % (recipient, message))

def mode(channel, recipient, mode):
    send("MODE %s %s %s" % (channel, mode, recipient))
