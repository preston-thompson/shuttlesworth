import random

word_db = dict()

def record_recurse(words, db):
    if not words:
        return
    if words[0] not in db:
        db[words[0]] = dict()
    if len(words) > 1:
        if words[1] not in db[words[0]]:
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
        depth = random.randint(1, 5)
        if word not in word_db:
            break
        db = word_db[word]
        for i in range(depth):
            if not db:
                break
            word = random.choice(list(db.keys()))
            message += word + " "
            db = db[word]
    return message
