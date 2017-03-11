import sys
import json
from random import shuffle


def limit(iterable, number=10):
    '''L3vi's trick'''
    for x, _ in zip(iterable, range(number)):
        yield x

def get_domain(url):
    if url:
        return url.split('/')[2]
    else:
        return None

if __name__ == '__main__':
    print("Reading JSON file...", file=sys.stderr)
    with open("recipes-withsteps.json") as f:
        recipes = [json.loads(line) for line in f]

    shuffle(recipes)

    print("Writing JSON file...", file=sys.stderr)
    with open("recipes-withsteps-shuffled.json", "w") as f:
        for recipe in recipes:
            f.write(json.dumps(recipe) + "\n")
