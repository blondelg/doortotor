import functools
from .utils import TorElements
from urllib.parse import urlencode
from urllib.parse import urlparse




from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('view', __name__, url_prefix='')

tor = TorElements()


@bp.route('/', methods=('GET', 'POST'))
def search():
    ctx = {}
    url = urlid = None

    if request.method == 'POST':
        url = request.form['url']

    if request.method == 'GET':
        urlid = request.args.get('urlid')

    # get response from url or urlid
    #tor.flush()
    tor.get_response(url, urlid)

    # get child page title
    ctx['title'] = tor.title

    # get child page head
    ctx['head'] = tor.head

    # get body
    ctx['body'] = tor.body

    return render_template('base.html', ctx=ctx)


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>', methods=('GET', 'POST'))
def path(path):
    ctx = {}
    url = urlid = None
    temp_query = urlencode(request.args)
    temp_path = urlparse(path)._replace(query=temp_query)

    if request.method == 'GET':
        urlid = request.args.get('urlid')

    # get response from url or urlid
    tor.get_response(url, urlid, temp_path)

    # get child page title
    ctx['title'] = tor.title

    # get child page head
    ctx['head'] = tor.head

    # get body
    ctx['body'] = tor.body

    return render_template('base.html', ctx=ctx)
