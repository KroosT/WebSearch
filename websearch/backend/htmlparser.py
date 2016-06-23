from bs4 import BeautifulSoup
import urlparse
from crawler import Crawler
import indexer
import re


class HtmlParser(object):

    def __init__(self, urls):
        self.urllist = urls
        self.cr = Crawler()
        self.title = ""
        self.text = ""

    def geturllist(self, response, soup):
        base = response.geturl()
        for link in soup.find_all('a'):
            parsed_link = urlparse.urldefrag(urlparse.urljoin(
                base, link.get('href')))[0].encode('ascii', 'ignore')
            if parsed_link not in self.urllist:
                self.urllist.append(parsed_link)

    def gettext(self, soup):
        for s in soup.find_all(['style', 'script', '[document]', 'head',
                                'title']):
            s.decompose()
        self.text = ' '.join(soup.get_text().split())

    def gettitle(self, soup):
        self.title = soup.title.string.encode('utf-8')

    def startcrawler(self):
        for url in self.urllist:
            print 'Visiting {}'.format(url)
            try:
                response = self.cr.open(url)
                soup = BeautifulSoup(response, 'html.parser')
                self.geturllist(response, soup)
                print 'Success'
            except:
                print 'Failed'

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

# urls = ['http://www.tut.by']
# h = HtmlParser(urls)
# h.startcrawler()
