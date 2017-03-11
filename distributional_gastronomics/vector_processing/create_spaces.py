from composes.semantic_space.space import Space
from composes.semantic_space.peripheral_space import PeripheralSpace
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting
from composes.transformation.dim_reduction.svd import Svd
from composes.utils import io_utils

import sys

print("Creating ingredient space...",end="",file=sys.stderr)
sys.stderr.flush()

ingredient_space = Space.build(data="ing2all.sm",
        rows="ing2all.rows",
        cols="ing2all.cols",
        format="sm")
print("Ingredient space is created.")

io_utils.save(ingredient_space, "ingredient_space.pkl")

print("Applying PPMI... ",end="", file=sys.stderr)
sys.stderr.flush()
ingredient_space = ingredient_space.apply(PpmiWeighting())
print("Applying SVD (20)... ",end="",file=sys.stderr)
sys.stderr.flush()
ingredient_space = ingredient_space.apply(Svd(20))
print("You got a reduced space. Done.", file=sys.stderr)

io_utils.save(ingredient_space, "ingredient_space.ppmi.svd20.pkl")


verb_space = Space.build(data="verb2all.sm",
        rows="verb2all.rows",
        cols="verb2all.cols",
        format="sm")
io_utils.save(verb_space, "verb_space.pkl")

print("Applying PPMI... ",end="", file=sys.stderr)
sys.stderr.flush()
verb_space = verb_space.apply(PpmiWeighting())
print("Applying SVD (50)... ",end="",file=sys.stderr)
sys.stderr.flush()
verb_space = verb_space.apply(Svd(50))
print("Verb space is reduced too. Done. ", file=sys.stderr)

io_utils.save(verb_space, "verb_space.ppmi.svd50.pkl")


