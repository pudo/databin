from flask import make_response
from StringIO import StringIO
from uuid import uuid4
import csv


def make_it_cache(res, timestamp):
    res.headers['Cache-Control'] = 'public; max-age: 86400'
    res.headers['Last-Modified'] = timestamp.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return res


def make_csv(table):
    data = StringIO()
    writer = csv.writer(data)
    for row in table:
        writer.writerow([v.encode('utf-8') for v in row])
    res = make_response(data.getvalue())
    res.headers['Content-Type'] = 'text/csv; encoding=utf-8'
    return res


def encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]


def decode(number):
    return int(number, 36)


def make_key():
    return uuid4().hex[:6]
