import random

word_db = dict()

def init(log):
    while 1:
        text = log.readline().rstrip()
        if not text:
            break
        record(text)

def record(text):
    words = text.split()

    for word_index, word in enumerate(words):
        if word_index == len(words) - 1:
            break
        next_word = words[word_index + 1]
        if word not in word_db:
            word_db[word] = dict()
        word_db[word][next_word] = dict()

def talk():
    word = random.choice(list(word_db.keys()))
    message = word + " "
    while len(message) < 400:
        #if random.randint(0, 15) == 0:
            #break
        if word not in word_db:
            break
        word = random.choice(list(word_db[word].keys()))
        message += word + " "

    return message
