PUNCTUATION = ' ,.?;!"\n'
def split(riddle, include_everything=True):
  riddle = riddle.replace('’', "'")
  if not include_everything:
    riddle = ' '.join([r for r in riddle.split('\n') if 'riddle by' not in r])
  res = []
  cur = ""
  for c in riddle:
    if c in PUNCTUATION:
      if cur:
        res.append(cur)
        cur = ""
      if include_everything:
        res.append(c)
    else:
      cur += c
  if cur:
    res.append(cur)
  return res