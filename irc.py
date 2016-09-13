import socket

sock = None
buf = str()

def send(s):
    print("sending: " + s)
    sock.send(bytes(s, "utf-8") + b"\r\n")

def receive():
    global buf
    while "\r\n" not in buf:
        text = sock.recv(1024).decode("utf-8")
        buf += text
        print("received: " + text)
    rv = buf[:buf.index("\r\n")]
    buf = buf[buf.index("\r\n") + 2:]
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
