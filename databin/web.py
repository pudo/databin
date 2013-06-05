from flask import render_template, request, redirect, url_for
from werkzeug.exceptions import NotFound
from formencode import Invalid, htmlfill

from databin.core import app, db
from databin.model import Paste


@app.route("/t/<key>")
def view(key):
    paste = Paste.by_key(key)
    if paste is None:
        raise NotFound('No such table: %s' % key)
    return render_template('view.html', paste=paste.to_dict())


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
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)
