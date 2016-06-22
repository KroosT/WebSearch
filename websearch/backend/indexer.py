import re


def words_positions(text):
    words = re.findall(ur'\w+', unicode(text).lower(), flags=re.UNICODE)
    word_pos = {}
    for index, word in enumerate(words):
        if word in word_pos:
            word_pos[word].append(index)
        else:
            word_pos[word] = [index]
    return word_pos
