import collections
import math
import re


class Indexer:

    def __init__(self, files):
        self.files = files
        self.words_in_file = {}
        self.index = {}
        self.build_index(self.files)
        self.tf = None
        self.idf = None
        self.tfidf = None

    @staticmethod
    def _words_positions(text):
        words = re.findall(ur'\w+', unicode(text).lower(), flags=re.UNICODE)
        word_pos = {}
        for index, word in enumerate(words):
            if word in word_pos:
                word_pos[word].append(index)
            else:
                word_pos[word] = [index]
        return word_pos

    def build_index(self, files):
        words_in_file = {}
        for filename in files:
            self.words_in_file[filename] = self._words_positions(
                open(filename, 'r').read())
        for filename in files:
            for word in files[filename].keys():
                if word in self.index:
                    self.index[word] = {filename: words_in_file[filename][word]}
                else:
                    self.index[word][filename] = words_in_file[filename][word]
        self._get_words_inverse_freq()

    def _one_word_query(self, word):
        word = re.match(ur'\w+', word, flags=re.UNICODE).group()
        if word in self.index:
            return self.index[word].keys()
        else:
            return []

    def _multiple_words_query(self, words):
        words = re.findall(ur'\b\w+\b', words, flags=re.UNICODE)
        result = []
        for word in words:
            result.extend(self._one_word_query(word))
        return result

    def phrase_query(self, query):
        words = re.findall(ur'\b\w+\b')
        results, files_list = [], []
        for word in words:
            files_list.append(self._one_word_query(word))
        shared_files = set(files_list[0]).intersection(*files_list)
        for filename in shared_files:
            words_positions = []
            for word in words:
                words_positions.append(self.index[word][filename])
            for i in xrange(len(words_positions)):
                for j in xrange(len(words_positions[i])):
                    words_positions -= i
            if set(words_positions[0]).intersection(*words_positions):
                results.append(filename)
        return self._rank_results(results, query)

    def _rank_results(self, results, query):
        query_vec = []
        pass

    def _get_term_freq(self, term, query):
        pass

    def _get_words_inverse_freq(self):
        ranked_index = collections.namedtuple('RankedIndex',
                                              ['files', 'inverse_freq'])
        for word in self.index:
            lt = math.log(len(self.files) / float(len(self.index[word])))
            self.index[word] = ranked_index(files=self.index[word].keys(),
                                            lt=lt)
