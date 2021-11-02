import numpy as np
import re
import csv
import json

def currency_parser(cur_str):
    '''
    Converts a variety of currencies into Floats with 2 places of precision for decimal currencies.

    Sourced From: Stack Overflow @ https://stackoverflow.com/questions/37580151/parse-currency-into-numbers-in-python
    '''
    # Remove any non-numerical characters
    # except for ',' '.' or '-' (e.g. EUR)
    cur_str = re.sub("[^-0-9.,]", '', cur_str)
    # Remove any 000s separators (either , or .)
    cur_str = re.sub("[.,]", '', cur_str[:-3]) + cur_str[-3:]

    if '.' in list(cur_str[-3:]):
        num = float(cur_str)
    elif ',' in list(cur_str[-3:]):
        num = float(cur_str.replace(',', '.'))
    else:
        num = float(cur_str)

    return np.round(num, 2)

db = {}

headers = []
# keep = ['title', 'original_title', 'description', 'avg_vote', 'votes', 'budget', 'usa_gross_income', 'worlwide_gross_income', 'director', 'writer', 'production_company', 'actors']
keep = ['original_title', 'avg_vote', 'votes', 'budget'] # Minified to reduce filesize
ints = ['votes']
floats = ['avg_vote']
monies = ['budget', 'usa_gross_income', 'worlwide_gross_income']

counter = 0
print('About to Read')
with open(input('Input Filename: '), newline='', encoding='utf-8') as f:
    print('Reading')
    csvreader = csv.reader(f)
    for row in csvreader:
        if counter == 0:
            headers = row[:]
        else:
            if row[headers.index('language')].lower() == 'english':
                db[row[headers.index('imdb_title_id')]] = {}
                for e in keep:
                    value = row[headers.index(e)]
                    if value == '':
                        db.pop(row[headers.index('imdb_title_id')])
                        break
                    if e in monies:
                        # if value[0] != '$': # Disabled this because csv format changed
                        #     db.pop(row[headers.index('imdb_title_id')])
                        #     break
                        value = currency_parser(value)
                    elif e in floats:
                        value = float(value)
                    elif e in ints:
                        value = int(value)
                    db[row[headers.index('imdb_title_id')]][e] = value
        counter += 1
print('Read Successfully')

print('About to Write')
with open(input('Output Filename: '), 'w', encoding='utf-8') as f:
    json.dump(db, f)
print('Written')
