import json, re
import sys

def log(*arg, **kw):
    print(*arg, file=sys.stderr, **kw)

STATE=''
title = ''
yield_ = ''
instructions = ''
ingredients = []
category = ''

def fix_ingredients(ingredients):
    bfr = None
    def decolumn(ceva):
        for element in ingredients:
            if element.startswith('---'):
                continue
            elif '      ' in element:
                yield from filter(bool, map(str.strip, element.split('      ')))
            else:
                yield element
    for element in decolumn(ingredients):
        if bfr and element.startswith('-'):
            bfr = bfr+element[1:]
        elif bfr:
            yield bfr
            bfr = element
        else:
            bfr = element
    if bfr:
        yield bfr


with open("NYC_all.mmf", 'r', encoding='latin-1') as f:
    for i, line in enumerate(f):
        line = line.strip()
        bad_beginnings = (
            'NOTE:',
            'Recipe:',
            'Contributor:',
            'Source:',
            'source:',
            'Posted by',
            'NB:',
            'Per serving:',
            'Exported from',
            'Translated by',
            '(C)',
            '©',
            '- - - - -',
            'Recipe By',
            )
        if 'Meal-Master' in line:
            if title and yield_ and instructions and ingredients:
                d = {}
                d['name'] = title
                d['recipeYield'] = yield_
                d['categories'] = categories
                d['instructions'] = instructions
                d['ingredients'] = '\n'.join(fix_ingredients(ingredients))
                print(json.dumps(d))
            STATE = 'header'
            title = ''
            yield_ = ''
            instructions = ''
            ingredients = []
            categories = []
        elif STATE == 'NONE':
            continue
        elif line.lower().startswith("title: "):
            title = line.split(":")[1].strip()
        elif line.lower().startswith("categories: "):
            categories_original = line.split(":")[1].strip().lower()
            # split on ',', '/', ' and ', '&'
            categories = list(map(
                str.strip,
                re.split('( and |&|/|,)', categories_original)[::2]
                ))

        elif line.lower().startswith("yield:") or line.lower().startswith("servings:"):
            yield_ = line.split(":")[1].strip()
        elif not line:
            if STATE == 'header':
                STATE = 'ingredients'
            elif STATE == 'ingredients' and ingredients:
                STATE = 'instructions'
        elif 'http' in line or line.startswith('-----'):
            STATE = 'NONE'
        elif any(line.startswith(that) for that in bad_beginnings):
            STATE = 'NONE'
        else:
            if STATE == 'instructions':
                dirty = False
                for bad in bad_beginnings:
                    if bad in line:
                        line = line.split(bad)[0]
                        dirty = True
                instructions += line
                if dirty:
                    STATE = 'NONE'
            elif STATE == 'ingredients':
                ingredients.append(line)
