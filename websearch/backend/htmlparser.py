from BeautifulSoup import BeautifulSoup
import urlparse
from crawler import Crawler
import indexer


class HtmlParser(object):

    def __init__(self, url):
        self.url = url
        self.cr = Crawler()
        self.response = self.cr.open(self.url)
        self.soup = BeautifulSoup(self.cr.open(self.url))
        self.urllist = []
        self.text = ""

    def geturllist(self):
        base = self.response.geturl()
        for link in self.soup.findAll('a'):
            self.urllist.append(urlparse.urldefrag(urlparse.urljoin(
                base, link.get('href')))[0].encode('ascii'))

    def gettext(self):
        for s in self.soup.findAll(['style', 'script', '[document]', 'head',
                                    'title']):
            s.decompose()
        self.text = ' '.join(self.soup.getText().split())


h = HtmlParser('http://pi-code.blogspot.com.by/2008/12/2.html')
h.geturllist()
h.gettext()
print h.text
print indexer.words_positions(h.text)
