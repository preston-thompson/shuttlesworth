import random

word_db = list()
end_word_db = list()
start_word_db = list()

def rand_geometric(min, max, alpha):
    z = (alpha ** (max + 1)) - 1
    c = random.randint(0, z - 1)
    start = min
    for i in range(0, max + 1):
        end = start + alpha ** (max - i)
        if start <= c and c < end:
            return i
        start = end

def record(text):
    words = text.split()
    start_word_db.append(words[0])
    end_word_db.append(words[-1])
    for i in range(0, len(words) - 1):
        if i >= len(word_db):
            word_db.append(dict())
        for word_index, word in enumerate(words):
            if word_index == len(words) - (i + 1):
                break
            if word not in word_db[i]:
                word_db[i][word] = list()
            word_db[i][word].append(words[word_index + 1:word_index + i + 2])

def talk(word, max_length):
    if word not in word_db[0]:
        word = random.choice(start_word_db)
    message = word + " "
    while len(message) < max_length:
        depth = rand_geometric(0, len(word_db) - 1, 2)
        while word not in word_db[depth] and depth >= 0:
            depth -= 1
        if depth < 0:
            break
        if word in end_word_db:
            if random.randint(0, 4) == 0:
                break
        next_words = random.choice(word_db[depth][word])
        for w in next_words:
            message += w + " "
        word = next_words[-1]
    return message
