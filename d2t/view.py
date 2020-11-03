from fake_useragent import UserAgent
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import functools
import requests



from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('view', __name__, url_prefix='')

@bp.route('/', methods=('GET', 'POST'))
def search():
    ctx = {}
    if request.method == 'POST':
        url = request.form['url']

    if request.method == 'GET':
        urlid = request.args.get('urlid')
        if urlid:
            page_refs = g.pop('page_refs', None)
            print("DEBUG :", page_refs)
            url = page_refs[urlid]
        else:
            return render_template('base.html', ctx=ctx)

    # create TorElements object
    tor = TorElements(url, session)

    # get child page title
    ctx['title'] = tor.get_title()

    # get child page head
    ctx['head'] = tor.get_head()

    # get body
    ctx['body'] = tor.get_body()

    return render_template('base.html', ctx=ctx)


class TorElements():

    """ Submit request over Tor network, parse response to fit into browser """

    def __init__(self, url, session):

        session['page_url'] = self.url = urlparse(url)
        self.response = self.get_response()

        self.html = self.response.text
        self.soup = self.get_soup()
        self.set_abs_href(session)
        self.body = self.get_body()

        self.title = self.get_title()

    def get_response(self):

        headers = { 'User-Agent': UserAgent().random }
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

        response = requests.get(self.url.geturl(), proxies=proxies, headers=headers)
        return response


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

    def set_abs_href(self, session):
        """ replace relatives hrefs to absolute ones """
        url_count = 1
        page_refs = {}
        for tag in self.soup.find_all():

            if tag.has_attr('href'):
                temp_url = urlparse(tag['href'])
                temp_url = self.normalize_url(temp_url, session)

            if tag.has_attr('src'):
                temp_url = urlparse(tag['src'])
                temp_url = self.normalize_url(temp_url, session)

            if tag.has_attr('href') and tag.name == 'a':
                page_refs[url_count] = temp_url.geturl()
                tag['href'] = f'/?urlid={url_count}'
                url_count += 1

            elif tag.has_attr('href') and tag.name == 'link':
                tag['href'] = temp_url.geturl()

            elif tag.has_attr('src'):
                tag['src'] = temp_url.geturl()

        g.page_refs = page_refs


    def normalize_url(self, url, session):
        """ from a given urlparse object, make sure scheme and netloc are correct """

        if not url.scheme:
            url = url._replace(scheme=session['page_url'].scheme)

        if not url.netloc:
            url = url._replace(netloc=session['page_url'].netloc)

        return url
