from StringIO import StringIO
import csv


def parse_cell(cell):
    try:
        return cell.decode('utf-8')
    except:
        return cell


def parse_csv(data, delimiter=','):
    databuf = StringIO(data.encode('utf-8'))
    rows = []
    for row in csv.reader(databuf, delimiter=delimiter):
        rows.append([parse_cell(c) for c in row])
    return False, rows


def parse_tsv(data):
    return parse_csv(data, delimiter='\t')


def parse_ssv(data):
    return parse_csv(data, delimiter=' ')
