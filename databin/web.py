import logging

from flask import render_template, request, redirect, url_for
from flask import make_response
from werkzeug.exceptions import NotFound, HTTPException
from formencode import Invalid, htmlfill

from databin.core import app
from databin.model import Paste
from databin.util import make_it_cache, make_csv, make_json
from databin.util import generate_etag, response_format
from databin.cors import crossdomain
from databin.parsers import get_parsers, ParseException, parse

log = logging.getLogger(__name__)

class NotModified(HTTPException):
    code = 304


def get_paste(key, format):
    paste = Paste.by_key(key)
    if paste is None:
        raise NotFound('No such table: %s' % key)
    etag = generate_etag(key, format)
    if request.if_none_match and request.if_none_match == etag:
        raise NotModified()
    has_header, table = False, None
    try:
        has_header, table = parse(paste.format, paste.data)
    except ParseException, pe:
        log.exception(pe)
    has_header = has_header or paste.force_header
    return paste, table, has_header, etag


@app.route("/t/<key>.<format>")
@app.route("/t/<key>")
@crossdomain(origin='*')
def view(key, format=None):
    format = response_format(format)
    paste, table, has_header, etag = get_paste(key, format)
    if format == 'json':
        res = make_json(table, has_header)
    elif format == 'csv':
        res = make_csv(table)
    else:
        html = render_template('view.html',
                               paste=paste.to_dict(),
                               has_header=has_header,
                               table=table)
        res = make_response(html)
    return make_it_cache(res, etag)


@app.route("/", methods=['POST'])
def post():
    try:
        paste = Paste.create(request.form, request.remote_addr)
        return redirect(url_for('view', key=paste.key))
    except Invalid, inv:
        return htmlfill.render(index(), auto_insert_errors=False,
                               defaults=request.form,
                               errors=inv.unpack_errors())


@app.route("/")
def index():
    return render_template('index.html',
                           parsers=get_parsers())


if __name__ == "__main__":
    app.run(port=5000)
