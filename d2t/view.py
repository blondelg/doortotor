import functools
from .utils import TorElements


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
    tor.get_response(url, urlid)

    # get child page title
    ctx['title'] = tor.title

    # get child page head
    ctx['head'] = tor.head

    # get body
    ctx['body'] = tor.body

    return render_template('base.html', ctx=ctx)
