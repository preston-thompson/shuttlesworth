#!/usr/bin/env python

import random
import sys

import config
import irc
import markov
import stocks

def main():
    state = {
        "stfu": False,
    }

    random.seed()

    log = open("log.txt", "r")
    while 1:
        text = log.readline().rstrip()
        if not text:
            break
        if config.nick not in text:
            markov.record(text)
    log.close()

    irc.connect(config.server, config.port, config.nick)
    irc.join(config.channel)

    while 1:
        text = irc.receive()
        words = text.split()

        if text.find("PING") == 0:
            irc.send("PONG " + words[1])
            continue

        if words[1] == "PRIVMSG" and words[2] == config.channel:
            message = text[text.index("PRIVMSG") + len("PRIVMSG " + config.channel + " :"):]
            message_words = message.split()

            if message.find("!%s" % config.nick) == 0 and len(message_words) > 1:
                if message_words[1] == "stfu":
                    irc.privmsg(config.channel, "ok")
                    state["stfu"] = True
                    continue

                elif message_words[1] == "talk":
                    irc.privmsg(config.channel, "ok")
                    state["stfu"] = False
                    continue

                elif message_words[1] == "state":
                    irc.privmsg(config.channel, str(state))
                    continue

                elif message_words[1] == "stock" and len(message_words) == 3:
                    irc.privmsg(config.channel, stocks.get_stock_info(message_words[2]))
                    continue

                elif message_words[1] == "op" and len(message_words) == 3:
                    irc.mode(config.channel, message_words[2], "+o")
                    continue

                else:
                    irc.privmsg(config.channel, "what?")
                    continue

            log = open("log.txt", "a")
            log.write(message + "\n")
            log.close()

            if config.nick not in message:
                markov.record(message)

            if not state["stfu"] and config.nick in message:
                word = random.choice(message_words)
                irc.privmsg(config.channel, markov.talk(word, config.max_length))
                continue

if __name__ == "__main__":
    main()
