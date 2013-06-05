from databin.parsers.util import ParseException
from databin.parsers.simple import parse_csv, parse_tsv
from databin.parsers.psql import parse_psql

PARSERS = [
    ('Excel copy & paste', 'excel', parse_tsv),
    ('Comma-Separated Values', 'csv', parse_csv),
    ('Tab-Separated Values', 'tsv', parse_tsv),
    ('psql Shell', 'psql', parse_psql),
]


def parse(format, data):
    for name, key, func in PARSERS:
        if key == format:
            return func(data)
    raise ParseException()


def get_parsers():
    for name, key, func in PARSERS:
        yield (key, name)
