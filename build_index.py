import csv
import sys
import json
index = []

def add_chars(st, data, num_chars):
  for i in range(0, len(st) - num_chars):
    data[st[i:i+num_chars]] = 1


with open('data.csv', newline='') as csvfile:
  r = csv.DictReader(csvfile)
  header = next(r)
  with open('values.csv', 'w', newline='') as w:
    x = r.fieldnames + ['Index']
    writer = csv.DictWriter(w, x)
    writer.writeheader()

    for row in r:
      data = {}
      row['Riddle'] = row['Riddle'].strip()
      st = row['Riddle'].lower().replace('\r\n','')
      row['Riddle'] = row['Riddle'].replace('\r\n','<br>')
      add_chars(st, data, 1)
      add_chars(st, data, 2)
      add_chars(st, data, 3)
      row['Index'] = json.dumps(data)
      writer.writerow(row)
    
    
      
    