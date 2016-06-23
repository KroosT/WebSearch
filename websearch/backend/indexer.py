import math


class Indexer:

    def __init__(self, words_in_files):
        self.words_in_files = words_in_files
        self.index = {}
        self.build_index()
        self.tf = {}
        self.compute_tf()
        self.idf = {}
        self.compute_idf()

    def build_index(self):
        for filename in self.words_in_files.keys():
            for word in self.words_in_files[filename].keys():
                if word in self.index:
                    self.index[word][filename] = (
                        self.words_in_files[filename][word])
                else:
                    self.index[word] = (
                        {filename: self.words_in_files[filename][word]})

    def compute_tf(self):
        for filename in self.words_in_files.keys():
            euclidean_norm = sum(
                [len(self.words_in_files[filename][word]) ** 2 for word
                 in self.words_in_files[filename].keys()]
            ) ** 0.5
            self.tf[filename] = {}
            for word in self.words_in_files[filename].keys():
                self.tf[filename][word] = (
                    len(self.words_in_files[filename][word]) / euclidean_norm)
        return self.tf

    def compute_idf(self):
        n = len(self.words_in_files)
        for word in self.index:
            self.idf[word] = math.log(n / len(self.index[word]))
        return self.idf
