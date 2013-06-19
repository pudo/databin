import logging

from flask import render_template, request, redirect, url_for
from flask import make_response
from werkzeug.exceptions import NotFound
from formencode import Invalid, htmlfill

from databin.core import app
from databin.model import Paste
from databin.util import make_it_cache, make_csv
from databin.parsers import get_parsers, ParseException, parse

log = logging.getLogger(__name__)


def get_paste(key):
    paste = Paste.by_key(key)
    if paste is None:
        raise NotFound('No such table: %s' % key)
    has_header, table = False, None
    try:
        has_header, table = parse(paste.format, paste.data)
    except ParseException, pe:
        log.exception(pe)
    return paste, table, has_header


@app.route("/t/<key>")
def view(key):
    paste, table, has_header = get_paste(key)
    html = render_template('view.html',
                           paste=paste.to_dict(),
                           has_header=has_header,
                           table=table)
    return make_it_cache(make_response(html),
                         paste.created_at)


@app.route("/c/<key>")
def view_csv(key):
    paste, table, has_header = get_paste(key)
    return make_it_cache(make_csv(table), paste.created_at)


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


for paste in Paste.all():
    if paste.key is None:
        from databin.util import encode
        from databin.core import db
        paste.key = encode(paste.id)
        db.session.add(paste)
        db.session.commit()


if __name__ == "__main__":
    app.run(port=5000)
