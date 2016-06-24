import urllib2
from robotparser import RobotFileParser
from urlparse import urlunsplit, urlsplit
from copy import copy
import sys
import socket

DEFAULT_CRAWLER_NAME = 'ryzhik'
DEFAULT_HEADERS = {
    'Accept': 'text/html, text/plain',
    'Accept-Charset': 'windows-1251, koi8-r, UTF-8, iso-8859-1, US-ASCII',
    'Content-Language': 'ru,en',
}
DEFAULT_EMAIL = 'anton.shestal.96@gmail.com'


class CheckRobotsPermission(urllib2.HTTPHandler):

    def __init__(self, crawlername, *args, **kwargs):

        urllib2.HTTPHandler.__init__(self, *args, **kwargs)
        self.crawlername = crawlername

    def http_open(self, req):

        url = req.get_full_url()
        host = urlsplit(url)[1]
        robots_url = urlunsplit(('http', host, '/robots.txt', '', ''))
        robotfileparser = RobotFileParser(robots_url)
        robotfileparser.read()
        if not robotfileparser.can_fetch(self.crawlername, url):
            raise RuntimeError('Forbidden by robots.txt')
        return urllib2.HTTPHandler.http_open(self, req)


class Crawler():

    def __init__(self, depth, width, crawlername=DEFAULT_CRAWLER_NAME,
                 new_headers={}, email=DEFAULT_EMAIL):

        self.depth = depth
        self.width = width
        self.crawlername = crawlername
        self.email = email
        self.opener = urllib2.build_opener(CheckRobotsPermission(
            self.crawlername))
        headers = copy(DEFAULT_HEADERS)
        headers.update(new_headers)
        opener_headers = [(k, v) for k, v in headers.iteritems()]
        if self.email:
            opener_headers.append(('From', email))
        self.opener.addheaders = opener_headers

    def open(self, url):
        self.depth -= 1
        return self.opener.open(url)
