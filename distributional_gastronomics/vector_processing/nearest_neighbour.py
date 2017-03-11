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

def ins(lst, el):
    if len(lst) < num:
        lst.append(el)
        lst.sort(reverse=True)
        return
    else:
        if el[0] > lst[-1][0]:
            lst.pop(-1)
            lst.append(el)
            lst.sort(reverse=True)

while True:
    inp = input("> ")
    if not inp:
        break
    inp = inp.replace(" ","_")
    if inp not in space.id2row:
        continue
    top = []
    for ing in space.id2row:
        if ing == inp or inp in ing:
            continue
        sim = space.get_sim(inp, ing, CosSimilarity())
        ins(top, (sim,ing))
    print("Nearest neighbors:",", ".join([x[1].replace("_"," ") + " (" + str(x[0]) + ")" for x in top]))
