import csv
import sys
import json
from collections import defaultdict
import math

from utils import split
index = []

class Riddle(object):

  def __init__(self, index, **kwargs):
    self.index = index
    self.kwargs = kwargs
  def __getattr__(self, name):
    return self.kwargs.get(name)
  def __repr__(self):
    #return f"{self.index}"
    return f"{self.index}: [{self.Answer}] {self.Riddle}"


location_map = {
  "Louise Hill": "LH",
  "3's Forest": "3F",
  "Silvie's Mine": "SM",
  "Aviar Cove": "AV",
  "Vaer Reef": "VR",
}

answer_images = {
  "Yellow / Tenacity": "tnc",
  "Red / Honor": "hnr",
  "Green / Charm": "crm",
  "Blue / Comprehension": "cmp",
}
def get_word_map(location):


  charm = defaultdict(list)
  ten = defaultdict(list)
  comp = defaultdict(list)
  honor = defaultdict(list)
  ans_dict = {
    'cmp': comp,
    'crm': charm,
    'tnc': ten,
    'hnr': honor
  }



  all_words = set()
  all_riddles = set()
  with open('data.csv', newline='', encoding='utf-8') as csvfile:
    r = csv.DictReader(csvfile)
    header = next(r)

    for i, row in enumerate(r):

      if row['Location'] != location: continue
      #row['Riddle'] = row['Riddle'].strip().lower().replace(',', ' ').replace('.', ' ').replace('?', ' ').replace(';', ' ').replace('!', ' ').replace('’', "'").replace('"', ' ')
      row['Riddle'] = ' '.join(split(row['Riddle'].strip().lower(), include_everything=False))
      ans = row['Answer']
      if ans == '?':
        continue
      r = Riddle(i, **dict(row))
      all_riddles.add(r)
      d = ans_dict[answer_images[ans]]
      #row['Riddle'] = ' '.join([r for r in row['Riddle'].split('\n') if 'riddle by' not in r])
      riddle = row['Riddle'].split()
      seen = set()
      for ch in riddle:
        if not ch:
          continue
        if ch in seen:
          continue
        seen.add(ch)
        all_words.add(ch)
        d[ch].append(r)


  def compute_purity(word):
    x = sorted([len(d[word]) for d in ans_dict.values()])
    if x[-2] > 2: return -1
    elif x[-2] == 0: return 10 + x[-1]
    else: return x[-1] - x[-2]
  def get_percentages(word):
    x = {}
    total = 0
    for k, d in ans_dict.items():
      a = len(d[word])
      if a:
        total += a
        x[k] = a
    x = {k: round(v/total*100) for k,v in x.items()}

    return x

  p = [(word, compute_purity(word), get_percentages(word)) for word in all_words]
  all_w = sorted(p, key=lambda x:x[1], reverse=True)
  top_words = [x[0] for x in p if x[1]>10]

  minimal_w = []
  def add_minimal_w(matcher, minimum):
    for w, c, d in all_w:
      if c < minimum:
        break
      key = sorted(list(d.keys()), key=lambda x:d[x], reverse=True)[0]
      riddles = ans_dict[key][w]
      if matcher([r in all_riddles for r in riddles]):
        minimal_w.append((w, d, c))
        for r in riddles:
          if r in all_riddles:
            all_riddles.remove(r)
  add_minimal_w(all, 10)
  if all_riddles:
    add_minimal_w(any, 10)
  if all_riddles:
    add_minimal_w(any, 1)
  add_minimal_w(lambda x: True, 10)
  if all_riddles:
    print(location, 'did not match all riddles:', all_riddles)
  return top_words, minimal_w

top_words = {}
word_counts = {}
for loc in location_map:
  location_short = location_map[loc]
  top_words[loc], word_counts[location_short] = get_word_map(loc)

with open('counts.json', 'w', encoding='utf-8') as w:
  json.dump(word_counts, w)


with open('top_words.json', 'w', encoding='utf-8') as w:
  json.dump(top_words, w)