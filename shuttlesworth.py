#!/usr/bin/env python

import random
import sys

import irc
import markov

stfu = False

def main():
    if len(sys.argv) != 5:
        print("usage: %s host port nick channel" % sys.argv[0])
        exit()

    server = sys.argv[1]
    port = int(sys.argv[2])
    nick = sys.argv[3]
    channel = sys.argv[4]

    random.seed()

    print("initializing...")
    log = open("log.txt", "r")
    markov.init(log)
    log.close()
    print("complete!")

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
            if username != nick:
                irc.send("MODE %s +o %s" % (channel, username))
            continue

        if words[1] == "PRIVMSG" and words[2] == channel:
            message = text[text.index("PRIVMSG") + len("PRIVMSG " + channel + " :"):]

            if message.find(nick) == 0:
                message_words = message.split()

                if len(message_words) > 1:
                    if message_words[1] == "stfu":
                        irc.send("PRIVMSG %s :ok" % channel)
                        stfu = True
                        continue

                    if message_words[1] == "talk":
                        irc.send("PRIVMSG %s :ok" % channel)
                        stfu = False
                        continue

            log = open("log.txt", "a")
            log.write(message)
            log.close()

            markov.record(message)

            if not stfu and (message.find(nick) != -1 or random.randint(0, 10) == 1):
                irc.send("PRIVMSG %s :%s" % (channel, markov.talk()))

            continue

if __name__ == "__main__":
    main()
