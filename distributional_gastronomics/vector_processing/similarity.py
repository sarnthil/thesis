import sys
from composes.utils import io_utils
from composes.similarity.cos import CosSimilarity
#from jaccard import JaccardSimilarity

if len(sys.argv) > 2:
    space = io_utils.load(sys.argv[2])
else:
    space = io_utils.load("ingredient_space.ppmi.svd20.pkl")

if len(sys.argv) > 1:
    num = int(sys.argv[1])
else:
    num = 1

while True:
    inp = input("1> ")
    if not inp:
        break
    inp2 = input("2> ")
    if not inp2:
        break
    inp = inp.replace(" ","_")
    if inp not in space.id2row:
        continue
    inp2 = inp2.replace(" ","_")
    if inp2 not in space.id2row:
        continue
    top = []
    sim = space.get_sim(inp, inp2, CosSimilarity())
    print("Similarity: {}".format(sim))
