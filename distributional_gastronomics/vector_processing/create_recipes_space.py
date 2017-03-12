import sys
import json
from itertools import count
from operator import itemgetter
from composes.utils import io_utils
from composes.composition.weighted_additive import WeightedAdditive
from composes.semantic_space.space import Space

def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

stacked_space = io_utils.load("ingredient_space.ppmi.svd20.pkl")

recipes = {}
max_size = 0
log("Reading recipes")
with open("NYC+openrecipes_cleanv1.jsonl") as f:
    for line in f:
        recipe = json.loads(line)
        ings = [ing['name'].lower().replace(' ', '_') for ing in recipe['ingredients']]
        rname = recipe['title'].lower().replace(' ', '_')
        recipes[rname] = ings
        if len(ings) > max_size:
            max_size = len(ings)

log("Starting addition...")
WA = WeightedAdditive(alpha = 1, beta = 1)
last_space = None
number = count()
for size in range(max_size,1,-1):
    log(f"Adding recipes of size {size}")
    relevant = (rec for rec in recipes if len(recipes[rec]) == size)
    composition = []
    for recipe in relevant:
        old = recipes[recipe]
        if size == 2:
            name = recipe
        else:
            name = "comp_" + str(next(number))
        # log('pre:', name, recipes[recipe][-5:])
        if old[-2] in stacked_space.id2row and old[-1] in stacked_space.id2row:
            composition.append((old[-1],old[-2],name))
            recipes[recipe].pop(-1)
            recipes[recipe].pop(-1)
            recipes[recipe].append(name)
        elif old[-1] not in stacked_space.id2row:
            recipes[recipe].pop(-1)
        else:
            # log('pop-pre:', name, recipes[recipe][-5:])
            recipes[recipe].pop(-2)
            # log('pop-post:', name, recipes[recipe][-5:])
        # log('post:', name, recipes[recipe][-5:])
    if composition:
        # log('composition:', composition)
        try:
            last_space = WA.compose(composition, stacked_space)
        except ValueError as e:
            log(recipe)
            raise e
        if size != 2:
            stacked_space = Space.vstack(stacked_space, last_space)

log("Dumping...")
io_utils.save(last_space, "recipe_space.pkl")
log("All done.")
