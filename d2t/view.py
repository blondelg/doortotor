import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('view', __name__, url_prefix='')

@bp.route('/', methods=('GET', 'POST'))
def request():

    return render_template('base.html')
