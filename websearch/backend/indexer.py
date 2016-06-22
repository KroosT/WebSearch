import re


def words_positions(text):
    text = text.lower()
    words = re.findall(r'\b[w]+\b', text)
    word_pos = {}
    for index, word in enumerate(words):
        if word in word_pos:
            word_pos[word].append(index)
        else:
            word_pos[word] = [index]
    return word_pos


def build_index(files):
    words_in_file = {}
    for filename in files:
        words_in_file[filename] = words_positions(open(filename, 'r').read())
    index = {}
    for filename in files:
        for word in files[filename].keys():
            if word in index:
                index[word] = {filename: words_in_file[filename][word]}
            else:
                index[word][filename] = words_in_file[filename][word]
    return index
