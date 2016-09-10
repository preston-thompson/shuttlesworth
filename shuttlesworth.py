#!/usr/bin/env python

import random
import sys

import irc

def main():
    if len(sys.argv) != 5:
        print("usage: %s host port nick channel" % sys.argv[0])
        exit()

    server = sys.argv[1]
    port = int(sys.argv[2])
    nick = sys.argv[3]
    channel = sys.argv[4]

    random.seed()

    irc.connect(server, port, nick)

    irc.send("JOIN %s" % channel)

    while 1:
        text = irc.receive()
        words = text.split()

        if text.find("PING") == 0:
            irc.send("PONG " + words[1])
            continue

        if words[1] == "JOIN":
            username = words[0][1:words[0].index("!")]
            irc.send("MODE %s +o %s" % (channel, username))
            continue

        if words[1] == "PRIVMSG" and words[2] == channel:
            message = text[text.index("PRIVMSG") + len("PRIVMSG " + channel + " :"):]
            log = open("log.txt", "a")
            log.write(message)
            log.close()
            continue

if __name__ == "__main__":
    main()
