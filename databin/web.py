import logging

from flask import render_template, request, redirect, url_for
from werkzeug.exceptions import NotFound
from formencode import Invalid, htmlfill

from databin.core import app
from databin.model import Paste
from databin.parsers import get_parsers, ParseException, parse

log = logging.getLogger(__name__)


@app.route("/t/<key>")
def view(key):
    paste = Paste.by_key(key)
    if paste is None:
        raise NotFound('No such table: %s' % key)
    has_header, table = False, None
    try:
        has_header, table = parse(paste.format, paste.data)
    except ParseException, pe:
        log.error("Failed to parse.")
    return render_template('view.html',
                           paste=paste.to_dict(),
                           has_header=has_header,
                           table=table)


@app.route("/", methods=['POST'])
def post():
    try:
        paste = Paste.create(request.form, request.remote_addr)
        return redirect(url_for('view', key=paste.key))
    except Invalid, inv:
        print inv.unpack_errors()
        return htmlfill.render(index(), auto_insert_errors=False,
                               defaults=request.form,
                               errors=inv.unpack_errors())


@app.route("/")
def index():
    return render_template('index.html',
                           parsers=get_parsers())


if __name__ == "__main__":
    app.run(port=5000)
