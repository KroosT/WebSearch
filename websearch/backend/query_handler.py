from websearch.models import WebPage
from websearch.models import Indexing
import math
import re


def handle_query(query):
    N = WebPage.objects.count()

    summary_len = 0
    for index in Indexing.objects.all():
        summary_len += index.frequency

    avgdl = summary_len / float(N)

    results = set()
    docs_with_word = {}
    words = set(re.findall(ur'\b\w+\b', query, flags=re.UNICODE))
    for word in words:
        docs = {elem.webpage for elem
                in Indexing.objects.filter(word__iexact=word)}
        docs_with_word[word] = len(docs)
        results = results.union(docs)
    results = list(results)
    return sorted(results, key=lambda doc: score(doc, docs_with_word, N, avgdl))


def score(doc, docs_with_word, N, avgdl):
    rank = 0
    for (word, n_docs) in docs_with_word.iteritems():
        try:
            freq = Indexing.objects.filter(word__iexact=word).\
                get(webpage=doc).frequency
        except:
            freq = 0
        rank += math.log((N-n_docs+0.5)/(n_docs+0.5), 2)*(
            freq*3/(freq+0.5+0.75*len(WebPage.objects.filter(id=doc.id))/avgdl))
