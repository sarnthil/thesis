import zipfile, shutil, os, sys

from glob import iglob as glob

print("")
for fname in glob("zips/*.zip"):
    print("\rExtracting from {}".format(fname[5:]), end='')
    zf = zipfile.ZipFile(fname, 'r')
    zf.extractall("wd")
    zf.close()
    for content in glob("wd/*"):
        if content.endswith(".mmf"):
            # Töpfchen
            shutil.move(content, 'mmf/{}'.format(content[3:]))
        else:
            # Kröpfchen
            shutil.move(content, 'rest/{}'.format(content[3:]))
