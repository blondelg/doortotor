from fake_useragent import UserAgent
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import functools
import requests



from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('view', __name__, url_prefix='')

@bp.route('/search/', methods=('GET', 'POST'))
def search():
    ctx = {}
    if request.method == 'POST':
        url = request.form['url']
        ctx = {}
        
        # create TorElements object
        tor = TorElements(url, session)
        print("DBEUG : ", session['url'])
        # get child page title
        ctx['title'] = tor.get_title()

        # get child page head
        ctx['head'] = tor.get_head()

        # get body
        ctx['body'] = tor.get_body()

    return render_template('base.html', ctx=ctx)


@bp.route('/clickon', methods=('GET', 'POST'))
def clickon():
    ctx = {}
    urlid = request.args.get('urlid')
    # get 


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
                print('DEBUG : ', urlparse(tag['href']))
                print('DEBUG : ', tag['href'])
            if tag.has_attr('href') and tag.name == 'a':
                page_refs[url_count] = tag['href']
                tag['href'] = f'/clickon?urlid={url_count}'
                url_count += 1

            elif tag.has_attr('href') and tag.name == 'link':
                tag['href'] = session['page_url'].scheme + "://" + session['page_url'].netloc + tag['href']

            elif tag.has_attr('src'):
                tag['src'] = session['page_url'].scheme + "://" + session['page_url'].netloc + tag['src']

        session['page_refs'] = page_refs




