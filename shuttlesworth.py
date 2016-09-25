#!/usr/bin/env python

import random
import sys

import irc
import markov

def main():
    if len(sys.argv) != 5:
        print("usage: %s host port nick channel" % sys.argv[0])
        exit()

    bot = {
        "stfu": False,
        "server": sys.argv[1],
        "port": int(sys.argv[2]),
        "nick": sys.argv[3],
        "channel": sys.argv[4],
        "log": "log.txt",
        "max_length": 400,
        "depth": 1,
    }

    random.seed()

    log = open("log.txt", "r")
    while 1:
        text = log.readline().rstrip()
        if not text:
            break
        if bot["nick"] not in text:
            markov.record(text)
    log.close()

    irc.connect(bot["server"], bot["port"], bot["nick"])
    irc.join(bot["channel"])

    while 1:
        text = irc.receive()
        words = text.split()

        if text.find("PING") == 0:
            irc.send("PONG " + words[1])
            continue

        # Give operator status to anyone who joins the channel.
        if words[1] == "JOIN":
            username = words[0][1:words[0].index("!")]
            if username != bot["nick"]:
                irc.mode(bot["channel"], username, "+o")
            continue

        if words[1] == "PRIVMSG" and words[2] == bot["channel"]:
            message = text[text.index("PRIVMSG") + len("PRIVMSG " + bot["channel"] + " :"):]
            message_words = message.split()

            if message.find("!%s" % bot["nick"]) == 0 and len(message_words) > 1:
                if message_words[1] == "stfu":
                    irc.privmsg(bot["channel"], "ok")
                    bot["stfu"] = True
                    continue

                if message_words[1] == "talk":
                    irc.privmsg(bot["channel"], "ok")
                    bot["stfu"] = False
                    continue

                if message_words[1] == "state":
                    irc.privmsg(bot["channel"], str(bot))
                    continue

            log = open("log.txt", "a")
            log.write(message + "\n")
            log.close()

            if bot["nick"] not in message:
                markov.record(message)

            if not bot["stfu"] and bot["nick"] in message:
                word = random.choice(message_words)
                while bot["nick"] in word and len(message_words) > 1:
                    word = random.choice(message_words)
                print(word)
                irc.privmsg(bot["channel"], markov.talk(word, bot["max_length"]))
                continue

if __name__ == "__main__":
    main()
