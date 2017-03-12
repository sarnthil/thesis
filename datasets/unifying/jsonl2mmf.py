import re
import json
import unicodedata

def format_ings(ings):
    '''      2 ts anise extract'''
    num = re.compile(r'[0-9 /.-]+')
    for ing in ings.split('\n'):
        ing = unicodedata.normalize('NFKC', ing)
        if ing[:len(ing)//2] == ing[len(ing)//2+1:]:
            yield 'DISCARD'
            raise StopIteration
        match = num.match(ing)
        if not match:
            continue
        f, u = match.span()
        number = ing[f:u]
        rest = ing[u:].strip()
        number = number.split("-")[0].strip()
        yield f'{number.rjust(7)} {rest}'


with open("recipes-minimal.json", 'r') as f:
    with open("recipes-minimal.mmf", 'w') as g:
        def p(*ce, **va):
            print(*ce, file=g, **va)
        for line in f:
            recipe = json.loads(line)
            recipe['ingr'] = '\n'.join(format_ings(recipe['ingredients']))
            if recipe['ingr'] == 'DISCARD':
                continue
            p('''----- gv Meal-Master

      Title: {name}
 Categories: None
      Yield: {recipeYield}

{ingr}

{instructions}

-----'''.format(**recipe))
