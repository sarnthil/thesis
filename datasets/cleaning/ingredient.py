import re
import sys
import json
from collections import namedtuple, Counter, defaultdict
from fractions import Fraction
from unidecode import unidecode
from textblob import Word
from multi_key_dict import multi_key_dict

Ingredient = namedtuple("Ingredient", "name amount modifiers plural")

units = re.compile(r'^(cubes?|cups?|c(a?ns?)?|[tT]|bulbs?|sprigs?|glass(es)?|dice|blocks?|an?|l|fl(uid)?\.?|ears?|lea(f|ves)|jars?|cartons?|strips?|heads?|wedges?|envelopes?|pints?|stalks?|sticks?|pinch(es)?|qts?|quarts?|handful|weight|bottles?|grinds?|tb\.?|lbs?\.?|oz\.?|mls?|g|cloves?|containers?|tablespoons?|teaspoons?|dash(es)?|pounds?|pinch|box(es)?|cans?|(milli)?lit[er]{2}s?|pkg\.?|pack(et)s?|packages?|whole|bars?|bags?|tbsps?\.?|tbs\.?|ts|tsps?\.?|ounces?|dash|pieces?|slices?|bunch(es)?|sticks?|fl\.?|gallons?|squares?|knobs?|grams?|kgs?|tub(es)?|kilograms?|tins?|%|drizzles?|splash(es)?|chunks?|inch(es)?)$')
number = re.compile(r'((\d+)?\.\d+|(\d+(/\d+)?-)?\d+(/\d+)?)')
blacklist = {'of', 'and', '&amp;', 'or', 'some', 'many', 'few', 'couple', 'as', 'needed', 'plus', 'more', 'to', 'serve', 'taste', 'x', 'in', 'cook', 'with', 'at', 'room', 'temperature', 'only', 'cover', 'length', 'into', 'if', 'then', 'out', 'preferably', 'well', 'good', 'better', 'best', 'about', 'all-purpose', 'all', 'purpose', 'recipe', 'ingredient', ')', '(', 'thick-', 'very', 'eating', 'lengthwise', 'each'}
parens = re.compile(r'[(\x97].*[)\x97]')
illegal_characters = re.compile(r'[‶″Â]')
cut_list = ['for', 'cut', 'such as']
replacements = {'yoghurt': 'yogurt', 'olife': 'olive', "'s": '', 'squeeze': 'squeezed', 'aubergine': 'eggplant', 'self raising': 'self-raising', 'pitta': 'pita', 'chile': 'chili'}

unit_conversions = multi_key_dict()
unit_conversions['pounds', 'pound', 'lbs', 'lb'] = ('g', 453.6)
unit_conversions['ounces', 'ounce', 'ozs', 'oz', 'weight'] = ('g', 28.35)
unit_conversions['can', 'cans', 'cn'] = ('can', 1)
unit_conversions['pints', 'pint', 'pts', 'pt'] = ('l', 0.4732)
unit_conversions['quarts', 'quart', 'qts', 'qt'] = ('l', 1.946352946)
unit_conversions['cups', 'cup', 'c'] = ('l', 0.2366)
unit_conversions['cubes', 'cube'] = ('cube', 1)
unit_conversions['fluid', 'fl'] = ('l', 0.02957)
unit_conversions['tablespoons', 'tablespoon', 'tbsps', 'tbsp', 'tb', 'tbs', 'T'] = ('l', 0.01479)
unit_conversions['teaspoons', 'teaspoon', 'tsps', 'tsp', 't', 'ts'] = ('l', 0.004929)
unit_conversions['milliliters', 'millilitres', 'ml'] = ('l', 0.001)
unit_conversions['gram', 'gs', 'grams'] = ('g', 1)
unit_conversions['kilogram', 'kgs', 'kg', 'kilograms'] = ('g', 0.001)

# tb, ts, t, T, can, cans, cn, c,

modifier_unifications = multi_key_dict()
modifier_unifications['nonfat', 'non-fat'] = 'fat-free'
modifier_unifications['low-fat', 'reduced-fat'] = 'fat-reduced'
modifier_unifications['flatleaf'] = 'flat-leaf'

with open("modifiers.txt") as f:
    modifiers = {line.strip() for line in f}
    modifiers.remove("lemon")
    modifiers.remove("garlic")
    modifiers.remove("almond")
    modifiers.remove("olive")
    modifiers.remove("half")
    modifiers.remove("sesame")
    modifiers.remove("chocolate")
    modifiers.add("kosher")
    modifiers.add("ripe")
    modifiers.add("mild")
    modifiers.add("quality")
    modifiers.add("commercial")
    modifiers.add("good-quality")
    modifiers.add("medium")
    modifiers.add("no-calories")
    modifiers.add("sea")
    modifiers.add("strong")
    modifiers.add("thai")
    modifiers.add("boneless")
    modifiers.add("seedless")
    modifiers.add("bittersweet")
    modifiers.add("english")
    modifiers.add("mature")
    modifiers.add("asian")
    modifiers.add("vegetable")
    modifiers.add("semi-sweet")
    modifiers.add("well-shaken")
    modifiers.add("bone-in")
    modifiers.add("semisweet")
    modifiers.add("torn")
    modifiers.add("homemade")
    modifiers.add("organic")
    modifiers.add("extra-virgin")
    modifiers.add("table")
    modifiers.add("fat-reduced")
    modifiers.add("reduced-fat")
    modifiers.add("gluten-free")
    modifiers.add("reduced-sodium")
    modifiers.add("low-sodium")
    modifiers.add("skinless")
    modifiers.add("squeezed")
    modifiers.add("low-fat")
    modifiers.add("full-fat")
    modifiers.add("nonfat")
    modifiers.add("celtic")
    modifiers.add("irish")
    modifiers.add("spanish")
    modifiers.add("hungarian")
    modifiers.add("american")
    modifiers.add("natural")
    modifiers.add("italian-style")
    modifiers.add("greek-style")
    modifiers.add("french-style")
    modifiers.add("country-style")
    modifiers.add("ranch-style")
    modifiers.add("louisiana-style")
    modifiers.add("dijon-style")
    modifiers.add("mexican-style")
    modifiers.add("miniature")
    modifiers.add("superfine")
    modifiers.add("fat-free")
    modifiers.add("non-fat")
    modifiers.add("free-range")
    modifiers.add("flat-leaf")
    modifiers.add("flatleaf")
    modifiers.add("broad")
    modifiers.add("self-raising")
    modifiers.add("fine-grain")
    modifiers.add("whole-grain")
    modifiers.add("fast-action")
    modifiers.add("part-skim")
    modifiers.add("extra-large")
    modifiers.add("whole-milk")
    modifiers.add("day-old")
    modifiers.add("lean")
    modifiers.add("extra-lean")
    modifiers.add("boiling-hot")
    modifiers.add("self-rising")
    modifiers.add("pure")
    modifiers.add("german")

def eprint(*foo, **bar):
    print(*foo, file=sys.stderr, **bar)

def make_fraction(string):
    if "-" in string:
        return Fraction(string.split("-")[0])
    return Fraction(string)

def lemmatize(word):
    if word in {
            'flour',
            'pita',
            'pita',
            'chia',
            'asparagus',
            'couscous',
            'ricotta',
            'ciabatta',
            'pancetta',
            'pasta',
            'burrata',
            'bruschetta',
            'hummus',
            'acacia',
            'tilapia',
            'macadamia',
            'feta',
            'polenta',
            'stevia',
            'passata',
            'philadelphia',
            'salata',
            'your',
            }:
        return word
    if word.endswith("i") and word != "octopi":
        return word
    return Word(word).singularize()

def normalize_ingredient(raw_name):
    num, unit, adjectives = 0, None, set()
    name = None
    plural = False
    raw_name = parens.sub("", raw_name).replace("half", "1/2")
    raw_name = raw_name.lower()
    for splitter in cut_list:
        if splitter in raw_name:
            raw_name = raw_name.split(splitter)[0]
    raw_name = illegal_characters.sub("", raw_name)
    raw_name = unidecode(raw_name).replace("_", " ").replace(',', '').strip()
    for replacement in replacements:
        raw_name = raw_name.replace(replacement, replacements[replacement])
    parts = raw_name.split()
    parts.reverse() # because pop(0) is terrible
    while parts:
        current = parts.pop()
        if current in blacklist or ":" in current:
            continue

        is_number = number.match(current)
        if is_number:
            if num == 0:
                if is_number.end() < len(current):
                    # unit included
                    num = make_fraction(current[:is_number.end()])
                    unit = current[is_number.end():]
                else:
                    num = make_fraction(current)
                    if parts and number.match(parts[-1]): # next token is also a number
                        # then we add the numbers
                        next_token = parts.pop()
                        is_number = number.match(next_token)
                        if is_number.end() < len(next_token):
                            # next token has a number
                            num += make_fraction(next_token[:is_number.end()])
                            unit = next_token[is_number.end():]
                        else:
                            num += make_fraction(next_token)
        elif units.match(current):
            if current in ('a','an'):
                if num == 0:
                    num = 1
            elif unit is None:
                unit = current
        elif current in modifiers or current[-2:] in ('ly', 'ed'):
            adjectives.add(modifier_unifications.get(current, current))
        else:
            lemma = lemmatize(current)
            if lemma != current:
                current = lemma
                plural = True
            if name:
                name += " " + current
            else:
                name = current
    num = float(num) if num else None
    if unit is not None and "/" in unit:
        unit = unit.split("/")[0]

    orig_num = num if num != 0 else None
    orig_unit = unit

    if unit in unit_conversions:
        unit, multiplier = unit_conversions[unit]
        if num is not None:
            num *= multiplier
    if name:
        return Ingredient(
                name=name,
                amount=(num if num!=0 else None, unit, orig_num, orig_unit),
                modifiers=list(adjectives),
                plural=plural,
                )
    else:
        return None


def collect_cooccurrences(output_cooc, output_mods, sep="\t"):
    eprint("Reading raw recipes")
    recipes = load_recipes()
    ing2ing = defaultdict(Counter)
    ing2mod = defaultdict(Counter)
    eprint("Collecting counts")
    for recipe in recipes:
        # TODO: filter most common ingredients, or only those in a list.
        ingredients = list(filter(bool, (normalize_ingredient(i) for i in recipes[recipe])))
        names = set(ing.name for ing in ingredients)
        for name in names:
            for co_name in names:
                ing2ing[name][co_name] += 1
        for ingredient in ingredients:
            for modifier in ingredient.modifiers:
                ing2mod[ingredient.name][modifier] += 1
    eprint("Writing co-occurrences with ingredients")
    with open(output_cooc, 'w') as f:
        for name in ing2ing:
            for co_name in ing2ing[name]:
                print(name, co_name, ing2ing[name][co_name], sep=sep, file=f)
    eprint("Writing co-occurrences with modifiers")
    with open(output_mods, 'w') as f:
        for name in ing2mod:
            for mod in ing2mod[name]:
                print(name, mod, ing2mod[name][mod], sep=sep, file=f)

def get_modifier_frequencies():
    recipes = load_recipes()
    modifiers = Counter()
    for recipe in recipes:
        for ingredient in recipes[recipe]:
            ing = normalize_ingredient(ingredient)
            if ing:
                modifiers.update(ing.modifiers)
    for i,j in modifiers.most_common():
        print(i, j, sep="\t")

def get_ingredient_frequencies():
    recipes = load_recipes()
    names = Counter()
    for recipe in recipes:
        for ingredient in recipes[recipe]:
            ing = normalize_ingredient(ingredient)
            if ing:
                names[ing.name] += 1
    for i,j in names.most_common():
        print(i, j, sep="\t")

def load_recipes():
    with open("raw_ingredients.json") as f:
        recipes = json.load(f)
    return recipes

if __name__ == '__main__':
    # collect_cooccurrences("ing2ing.sm", "ing2mod.sm")
    #get_modifier_frequencies()
    ...
