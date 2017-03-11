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

verb_space = Space.build(data="verb2all.sm",
        rows="verb2all.rows",
        cols="verb2all.cols",
        format="sm")
io_utils.save(verb_space, "verb_space.pkl")

