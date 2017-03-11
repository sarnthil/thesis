import json
from collections import Counter

definition = """chinese+china,mexican,italian,indian+india,german,jewish,spanish,canadian+french can,japanease,asian,irish,caribbean,middle east,indonesian,vietnamese,polish,russian,british+english,hungarian+hungary,oriental,thai+thailand,greek,turkish,american+so. america+america+new orleans+new york,korean,european+west europe,african,morocan,swedish,hawaiian,israeli,filipino,french,french,australian,american+newyork+country wom+country"""

mapping = {}
for synonyms in definition.split(","):
    synonyms = synonyms.split("+")
    for syn in synonyms:
        mapping[syn] = synonyms[0]

cats = Counter()

with open("NYC+categories.jsonl") as f:
    for line in f:
        for cat in json.loads(line)['categories']:
            if cat not in mapping: continue
            cats[mapping.get(cat, cat)] += 1

for count, value in cats.most_common(50):
    print(count, value, sep=",")
