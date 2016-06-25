from bs4 import BeautifulSoup
import urlparse
from crawler import Crawler
import re
from websearch.models import *
from multiprocessing import JoinableQueue
from websearch.tools import tools
import threading
# import multiprocessing as m

NUMBER_OF_THREADS = 4


class HtmlParser(object):

    crawled_file = ''
    urls_file = ''

    def __init__(self, urls):
        self.urllist = set(urls)
        self.cr = Crawler(2, 1)
        self.title = ""
        self.text = ""
        self.word_pos = {}
        self.queue = JoinableQueue()
        self.crawled = set()
        HtmlParser.crawled_file = 'crawled_links.txt'
        HtmlParser.urls_file = 'urls.txt'
        tools.set_to_file(self.urllist, HtmlParser.urls_file)

    def geturllist(self, response, soup):
        base = response.geturl()
        i = 0
        for link in soup.find_all('a'):
            if i > self.cr.width:
                break
            parsed_link = urlparse.urldefrag(urlparse.urljoin(
                base, link.get('href')))[0].encode('ascii', 'ignore')
            if parsed_link not in self.urllist:
                self.urllist.add(parsed_link)
                i += 1

    def gettext(self, soup):
        for s in soup.find_all(['style', 'script', '[document]', 'head',
                                'title']):
            s.decompose()
        self.text = ' '.join(soup.get_text().split())

    def gettitle(self, soup):
        self.title = soup.title.string.encode('utf-8')

    def startcrawler(self, url):
        if url not in self.crawled:
            self.urllist.remove(url)
            self.crawled.add(url)
            response = self.cr.open(url)
            soup = BeautifulSoup(response, 'html.parser')
            self.gettitle(soup)
            self.gettext(soup)
            self.word_pos = self._words_positions(self.text)
            if self.cr.depth > 0:
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
            self.update_files()

    def create_workers(self):
        for _ in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work)
            t.daemon = True
            t.start()

    def work(self):
        while True:
            url = self.queue.get()
            self.startcrawler(url)
            self.queue.task_done()

    def create_jobs(self):
        for link in tools.file_to_set(HtmlParser.urls_file):
            self.queue.put(link)
        self.queue.join()
        self.multiproc()

    def multiproc(self):
        if len(self.urllist) > 0:
            self.create_jobs()

    def update_files(self):
        tools.set_to_file(self.crawled, HtmlParser.crawled_file)
        tools.set_to_file(self.urllist, HtmlParser.urls_file)


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
