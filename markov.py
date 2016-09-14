import json
import random

word_db = dict()

def record_recurse(words, db):
    if len(words) < 2:
        return
    if words[0] not in db:
        db[words[0]] = dict()
    db[words[0]][words[1]] = dict()
    record_recurse(words[2:], db[words[0]][words[1]])

def record(text):
    words = text.split()

    for word_index, word in enumerate(words):
        if word_index == len(words) - 1:
            break

        if word not in word_db:
            word_db[word] = dict()

        record_recurse(words[word_index:], word_db)

def talk(word, max_length):
    if word not in word_db:
        word = random.choice(list(word_db.keys()))
    message = word + " "
    while len(message) < max_length:
        if word not in word_db:
            break
        word = random.choice(list(word_db[word].keys()))
        message += word + " "
        if word not in word_db:
            break
        db = word_db[word]
        depth = 0
        for i in range(0, depth):
            word = random.choice(list(db.keys()))
            message += word + " "
            if word not in db:
                break
            db = word_db[word]

    return message
