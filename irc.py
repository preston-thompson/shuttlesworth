import socket

sock = None
recv_buf = bytes()

def send(s):
    print("sending: " + s)
    sock.send(bytes(s, "utf-8") + b"\r\n")

def receive():
    text = sock.recv(1024)
    print("received: " + text[:-2].decode("utf-8"))
    return text.decode("utf-8")

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
