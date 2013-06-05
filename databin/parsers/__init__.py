from databin.parsers.util import ParseException
from databin.parsers.simple import parse_csv, parse_tsv

PARSERS = [
    ('Comma-Separated Values', 'csv', parse_csv),
    ('Tab-Separated Values', 'tsv', parse_tsv),
    ('Excel copy & paste', 'excel', parse_csv),
    ('psql Shell', 'psql', parse_csv),
]


def parse(format, data):
    pass


def get_parsers():
    for name, key, func in PARSERS:
        yield (key, name)
