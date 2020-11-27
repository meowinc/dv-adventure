import csv
import sys
import json
from utils import split
index = []

def add_chars(st, data, num_chars):
  for i in range(0, len(st) - num_chars):
    data[st[i:i+num_chars]] = 1

with open('top_words.json', 'r', encoding='utf-8') as f:
  top_words = json.load(f)

with open('data.csv', newline='') as csvfile:
  r = csv.DictReader(csvfile)
  with open('values.csv', 'w', newline='') as w:
    x = r.fieldnames + ['Index']
    writer = csv.DictWriter(w, x)
    writer.writeheader()

    for row in r:
      data = {}
      row['Riddle'] = row['Riddle'].strip()
      st = row['Riddle'].lower().replace('\r\n','')
      add_chars(st, data, 1)
      add_chars(st, data, 2)
      add_chars(st, data, 3)

      row['Riddle'] = row['Riddle'].replace('\r\n','\n')
      riddle = split(row['Riddle'])
      for n in range(len(riddle)):
        if riddle[n] == '\n':
          riddle[n] = '<br>'
        elif riddle[n] in top_words[row['Location']]:
          riddle[n] = '<spe>{}</spe>'.format(riddle[n])
      import pdb
      #pdb.set_trace()
      row['Riddle'] = ''.join(riddle)


      row['Index'] = json.dumps(data)
      writer.writerow(row)

