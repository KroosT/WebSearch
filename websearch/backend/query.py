from collections import defaultdict
import re


class QueryHandler:

    def __init__(self, indexer):
        self.indexer = indexer

    @staticmethod
    def dot_product(vec1, vec2):
        if len(vec1) != len(vec2):
            return 0
        else:
            sum([x*y for x, y in zip(vec1, vec2)])

    def rank_results(self, terms, results):
        files_vectors = defaultdict(lambda: [0]*len(terms))
        query_vector = [0]*len(terms)
        for term_index, term in enumerate(terms):
            if term in self.indexer.index:
                query_vector[term_index] = self.indexer.idf[term]
                for filename in self.indexer.index[term].keys():
                    if filename in results:
                        files_vectors[filename][term_index] = (
                            self.indexer.tf[filename][term])
        files_scores = (
            {self.dot_product(files_vectors[filename], query_vector): filename
             for filename in files_vectors.keys()})
        return sorted(files_scores.iteritems(), key=lambda (key, val): key)

    def one_word_query(self, word):
        word = re.match(ur'\w+', word, flags=re.UNICODE).group()
        if word in self.indexer.index:
            return self.indexer.index[word].keys()
        else:
            return []

    def free_text_query(self, text):
        words = re.findall(ur'\b\w+\b', text, flags=re.UNICODE)
        results = []
        for word in words:
            results.extend(self.one_word_query(word))
        return self.rank_results(words, results)

    def phrase_query(self, query):
        words = re.findall(ur'\b\w+\b', query)
        results, files_list = [], []
        for word in words:
            files_list.append(self.one_word_query(word))
        shared_files = set(files_list[0]).intersection(*files_list)
        for filename in shared_files:
            words_positions = []
            for word in words:
                words_positions.append(self.indexer.index[word][filename])
            for i in xrange(len(words_positions)):
                for j in xrange(len(words_positions[i])):
                    words_positions[i] -= i
            if set(words_positions[0]).intersection(*words_positions):
                results.append(filename)
        return results
