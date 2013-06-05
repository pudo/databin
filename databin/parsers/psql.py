

def clean(cell):
    return cell.strip()


def parse_psql(data):
    header, rows = False, []
    for row in data.split('\n'):
        if set(row.strip()) == set(('+', '-')):
            header = True
            continue
        cells = map(clean, row.split('|'))
        rows.append(cells)
    return header, rows
