from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fake_useragent import UserAgent
import hashlib

import requests


class TorElements():

    """ Submit request over Tor network, parse response to fit into browser """

    def __init__(self):

        pass


    def get_response(self, url='', urlid=None):

        if url:
            self.url = urlparse(url)
        elif urlid:
            print(type(urlid), urlid)
            self.url = self.page_refs[urlid]
        else:
            self.body = ''
            self.title = 'Accueil'
            self.head = ''
            return

        headers = { 'User-Agent': UserAgent().random }
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

        response = requests.get(self.url.geturl(), proxies=proxies, headers=headers)

        self.html = response.text
        self.soup = self.get_soup()
        self.set_abs_href()
        self.body = self.get_body()
        self.title = self.get_title()
        self.head = self.get_head()


    def get_title(self):
        """ from response, parse title """
        return self.soup.title.text

    def get_head(self):
        """ from soup retunrs head content """
        return '\n    '.join([str(e) for e in self.soup.head.findChildren() if
            e.name != 'title'])

    def get_body(self):
        """ get body tag from child page """
        return self.soup.body

    def get_soup(self):
        """ build the beautiful soup object """
        return BeautifulSoup(self.html, 'html.parser')

    def set_abs_href(self):
        """ replace relatives hrefs to absolute ones """
        url_count = 1
        self.page_refs = {}
        for tag in self.soup.find_all():

            if tag.has_attr('href'):
                temp_url = urlparse(tag['href'])
                temp_url = self.normalize_url(temp_url)

            if tag.has_attr('src'):
                temp_url = urlparse(tag['src'])
                temp_url = self.normalize_url(temp_url)

            if tag.has_attr('href') and tag.name == 'a':
                self.page_refs[str(url_count)] = temp_url
                tag['href'] = f'/?urlid={url_count}'
                url_count += 1

            elif tag.has_attr('href') and tag.name == 'link':
                tag['href'] = temp_url.geturl()

            elif tag.has_attr('src'):
                tag['src'] = temp_url.geturl()


    def normalize_url(self, url):
        """ from a given urlparse object, make sure scheme and netloc are correct """

        if not url.scheme:
            url = url._replace(scheme=self.url.scheme)

        if not url.netloc:
            url = url._replace(netloc=self.url.netloc)

        return url


    def get_md5(self, string):
        """ from a given string, returns md5 hash """
