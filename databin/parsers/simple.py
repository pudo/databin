from StringIO import StringIO
import csv


def parse_csv(data, delimiter=','):
    databuf = StringIO(data)
    rows = []
    for row in csv.reader(databuf, delimiter=delimiter):
        rows.append(row)
    return False, rows



def parse_tsv(data):
    return parse_csv(data, delimiter='\t')
