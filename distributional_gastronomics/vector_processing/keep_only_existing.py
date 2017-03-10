import sys
import shutil

with open("ing2ing.rows") as f:
    ings = {line.strip() for line in f}

if len(sys.argv) < 2:
    print("Gimme gimme gimme that name of the file there")
    sys.exit(1)

subtype = sys.argv[1]

with open(f"ing2{subtype}.sm") as f:
    with open(f"ing2{subtype}.sm.new", "w") as g:
        for line in f:
            ing, other, count = line.split("\t")
            if ing in ings:
                g.write(line)
shutil.move(f"ing2{subtype}.sm.new", f"ing2{subtype}.sm")
