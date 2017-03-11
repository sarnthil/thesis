import re
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup as Soup
from collections import defaultdict, Counter
from extraction import extractors, get


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
    print("Starting to crawl...", file=sys.stderr)
    try:
        for recipe in recipes:
            if "instructions" in recipe:
                print("Skipping recipe; already crawled", file=sys.stderr)
                continue
            url = recipe["url"]
            domain = get_domain(url)
            if domain is None:
                continue
            print("Downloading", url, file=sys.stderr)
            #sleep(0.02)
            try:
                r = get(url)
            except Exception:
                continue #skip this one for now
            if r.status_code != 200 and not (r.status_code == 404 and domain == 'www.aspicyperspective.com'):
                print("Error with this one.", file=sys.stderr)
                continue
            sp = Soup(r.text)
            try:
                instructions = extractors[domain](sp, url)
            except:
                continue
            if instructions is None:
                continue
            recipe["instructions"] = instructions
    except BaseException as e: # even BaseException (KeyboardInterrupt, ...)
        print("Error:", repr(e), file=sys.stderr)
    finally:
        print("Writing JSON file...", file=sys.stderr)
        with open("recipes-withsteps.json", "w") as f:
            for recipe in recipes:
                f.write(json.dumps(recipe) + "\n")
