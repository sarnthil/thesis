import json
from collections import Counter
import code

categories = Counter()

with open ("NYC+categories.jsonl") as f:
    for line in f:
        recipe = json.loads(line)
        for category in recipe['categories']:
            categories[category] += 1
code.interact(local=locals())

