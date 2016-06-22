import re


def words_positions(text):
    words = set(re.sub('[\W_]+', ' ', text.lower()).split())
    word_pos = {}
    for word in words:
        word_pos[word] = [m.start() for m
                          in re.finditer(r'\b%s\b' % word, text)]
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
