from bs4 import BeautifulSoup
import urlparse
from crawler import Crawler
import re
from websearch.models import *


class HtmlParser(object):

    def __init__(self, urls):
        self.urllist = urls
        self.cr = Crawler(3, 3)
        self.title = ""
        self.text = ""
        self.word_pos = {}

    def geturllist(self, response, soup):
        base = response.geturl()
        for link in soup.find_all('a'):
            for i in xrange(self.cr.width):
                parsed_link = urlparse.urldefrag(urlparse.urljoin(
                    base, link.get('href')))[0].encode('ascii', 'ignore')
                if parsed_link not in self.urllist:
                    self.urllist.append(parsed_link)
                    i -= 1

    def gettext(self, soup):
        for s in soup.find_all(['style', 'script', '[document]', 'head',
                                'title']):
            s.decompose()
        self.text = ' '.join(soup.get_text().split())

    def gettitle(self, soup):
        self.title = soup.title.string.encode('utf-8')

    def startcrawler(self):
        for url in self.urllist:
            try:
                # print 'Visiting {}'.format(url)
                response = self.cr.open(url)
                soup = BeautifulSoup(response, 'html.parser')
                self.gettitle(soup)
                self.gettext(soup)
                self.word_pos = self._words_positions(self.text)
                if self.cr.depth != 0:
                    self.geturllist(response, soup)
                page = WebPage(url=url, title=self.title, text=self.text,
                               indexed=False)
                page.save()
                for (word, list_pos) in self.word_pos.iteritems():
                    index = Indexing.objects.create(
                        word=word, frequency=len(list_pos), webpage=page)
                    index.save()

                page.indexed = True
                page.save()
                #print 'Success'
            except Exception:
                raise Exception


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
