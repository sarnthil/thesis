from composes.semantic_space.space import Space
from composes.semantic_space.peripheral_space import PeripheralSpace
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting
from composes.transformation.dim_reduction.svd import Svd
from composes.utils import io_utils

import sys

event_space = Space.build(data="verb2all.sm",
        rows="verb2all.rows",
        cols="verb2all.cols",
        format="sm")
io_utils.save(event_space, "event_space.pkl")

print("Applying PPMI... ",end="", file=sys.stderr)
sys.stderr.flush()
event_space = event_space.apply(PpmiWeighting())
print("Applying SVD (50)... ",end="",file=sys.stderr)
sys.stderr.flush()
event_space = event_space.apply(Svd(50))
print("Event space is reduced too. Done. ", file=sys.stderr)

io_utils.save(event_space, "event_space.ppmi.svd50.pkl")


