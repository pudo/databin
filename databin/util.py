from flask import make_response, request
from StringIO import StringIO
from uuid import uuid4
from hashlib import sha1
import csv
import json


FORMATS = {
    'application/json': 'json',
    'text/csv': 'csv',
    'text/html': 'html'
    }


def response_format(url_format):
    if url_format is not None and url_format in FORMATS.values():
        return url_format
    best_mime = request.accept_mimetypes.best_match(FORMATS.keys(),
            default='text/html')
    return FORMATS.get(best_mime)


def make_it_cache(res, etag):
    res.headers['Cache-Control'] = 'public; max-age: 8640000'
    res.headers['ETag'] = etag
    return res


def generate_etag(key, format):
    buf = '%s//%s//%s' % (key, format, request.args.get('callback'))
    return '"%s"' % sha1(buf).hexdigest()


def make_csv(table):
    data = StringIO()
    writer = csv.writer(data)
    for row in table:
        writer.writerow([v.encode('utf-8') for v in row])
    res = make_response(data.getvalue())
    res.headers['Content-Type'] = 'text/csv; encoding=utf-8'
    return res


def make_json(table, has_header):
    data = {'header': [], 'rows': list(table)}
    if has_header and len(data['rows']):
        data['header'] = data['rows'][0]
        data['rows'] = data['rows'][1:]
    data = json.dumps(data)
    if 'callback' in request.args:
        data = '%s && %s(%s);' % (request.args.get('callback'), 
                request.args.get('callback'), data)
    res = make_response(data)
    res.headers['Content-Type'] = 'application/json; encoding=utf-8'
    return res


def make_key():
    return uuid4().hex[:6]
