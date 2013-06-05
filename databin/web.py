from flask import render_template, request
from werkzeug.exceptions import NotFound
from formencode import Invalid

from databin.core import app, db
from databin.model import Paste


@app.route("/<key>")
def view(key):
    paste = Paste.by_key(key)
    if paste is None:
        raise NotFound('Not found!')
    return render_template('view.html', paste=paste.to_dict())


@app.route("/", methods=['POST'])
def post():
    pass


@app.route("/")
def index():
    print dir(request)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)
