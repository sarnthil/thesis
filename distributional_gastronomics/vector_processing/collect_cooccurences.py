import sys
import json
import re
import csv
from collections import Counter, defaultdict

ing2ing = defaultdict(Counter)
ing2mod = defaultdict(Counter)
ing2unit = defaultdict(Counter)
ing2verb = defaultdict(Counter)
ends = {' --', ' -', '&'}
starts = {'pk ', 'lg ', 'ea ', 'd ', 'md ', 'sm ', '&', '-'}
verb2verb = defaultdict(Counter)
verb2word = defaultdict(Counter)


def process_ing(name):
    name = name.replace(";", "")
    if any(name.endswith(end) for end in ends):
        name = " ".join(name.split()[:-1])
    if any(name.startswith(start) for start in starts):
        name = " ".join(name.split()[1:])
    return name.strip()

def get_ingredient_frequencies():
    recipes = load_recipes()
    for recipe in recipes:
        for ing1 in recipe['ingredients']:
            ing1 = process_ing(ing1['name'])
            if not ing1: continue
            for ing2 in recipe['ingredients']:
                ing2 = process_ing(ing2['name'])
                if not ing2: continue
                ing2ing[ing1][ing2] += 1
    for i in ing2ing:
        for j in ing2ing[i]:
            print(i, j, ing2ing[i][j], sep="\t")

def load_recipes():
    with open("NYC+openrecipes_cleanv1.jsonl") as f:
        for line in f:
            yield json.loads(line)

def load_events():
    with open("all_events.txt") as f:
        reader = csv.reader(f)
        yield from reader

def get_modifier_frequencies():
    recipes = load_recipes()
    for recipe in recipes:
        for ing in recipe['ingredients']:
            ing_name = process_ing(ing['name'])
            if not ing_name: continue
            for modifier in ing['modifiers']:
                ing2mod[ing_name]['mod_' + modifier] += 1
    for i in ing2mod:
        for j in ing2mod[i]:
            print(i, j, ing2mod[i][j], sep="\t")

def get_unit_frequencies():
    recipes = load_recipes()
    for recipe in recipes:
        for ing in recipe['ingredients']:
            ing_name = process_ing(ing['name'])
            if not ing_name: continue
            unit = ing['amount']['orig_unit']
            if unit is None:
                unit = "self"
            ing2unit[ing_name]['unit_' + unit] += 1
            if ing['plural']:
                ing2unit[ing_name]['plural_yes'] += 1
            else:
                ing2unit[ing_name]['plural_no'] += 1
    for i in ing2unit:
        for j in ing2unit[i]:
            print(i, j, ing2unit[i][j], sep="\t")

def get_verb_frequencies():
    verbs = set()
    with open("verbs") as v:
        for line in v:
            verb, _ = line.split()
            verbs.add(verb)
    recipes = load_recipes()
    for recipe in recipes:
        for ing in recipe['ingredients']:
            ing_name = process_ing(ing['name'])
            if not ing_name: continue
            recipe_steps = ' '.join(recipe['steps'])
            for verb in filter(lambda x: x in verbs, re.split('[^A-Za-z]+', recipe_steps)):
                ing2verb[ing_name][verb] += 1
    for i in ing2verb:
        for j in ing2verb[i]:
            print(i, j, ing2verb[i][j], sep="\t")

def get_verb2verb_frequencies():
    verbs = set()
    with open("verbs") as v:
        for line in v:
            verb, _ = line.split()
            verbs.add(verb)
    eventlists = load_events()
    for sentences in eventlists:
        all_verbs = list(filter(lambda x: x in verbs, re.split('[^A-Za-z]+', ' '.join(sentences))))
        for v1 in all_verbs:
            for v2 in all_verbs:
                verb2verb[v1][v2] += 1
        # for ing in recipe['ingredients']:
        #     ing_name = process_ing(ing['name'])
        #     if not ing_name: continue
        #     recipe_steps = ' '.join(recipe['steps'])
        #     for verb in filter(lambda x: x in verbs, re.split('[^A-Za-z]+', recipe_steps)):
        #         ing2verb[ing_name][verb] += 1
    for i in verb2verb:
        for j in verb2verb[i]:
            print(i, j, verb2verb[i][j], sep="\t")

def get_verb2word_frequencies():
    verbs = set()
    with open("verbs") as v:
        for line in v:
            verb, _ = line.split()
            verbs.add(verb)
    eventlists = load_events()
    for sentences in eventlists:
        for event in sentences:
            words = re.split('[^A-Za-z]+', event)
            verb = words[1].lower()
            if verb not in verbs: continue
            for word in words:
                if word:
                    verb2word[verb][word.lower()] += 1
    for i in verb2word:
        for j in verb2word[i]:
            print(i, j, verb2word[i][j], sep="\t")

if __name__ == '__main__':
    # get_ingredient_frequencies()
    # get_modifier_frequencies()
    # get_unit_frequencies()
    # get_verb_frequencies()
    # get_verb2verb_frequencies()
    get_verb2word_frequencies()
