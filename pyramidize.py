#!/usr/bin/env python

import os
import errno
from shutil import copyfile

indir = "/Volumes/Secondary/Namibia/Naukluft-maps/sat_tiles"
outdir = "tiles"

def zoom(z):
    z = int(z)
    z = -(z+2)+19
    return str(z)

try:
    os.mkdir(outdir)
except OSError as err:
    pass

stupid = lambda x: x == ".DS_Store"

dl = len(indir.split("/"))

# Change files from GMapCatcher format into classic z/x/y format
# Tiles start in top-left presumably
for root, subfolders, files in os.walk(indir):

    stupid_files = [f for f in files if stupid(f)]
    for f in stupid_files:
        os.remove(os.path.join(root,f))

    if len(files) == 0: continue
    r = root.split("/")[dl:]

    z = zoom(r[0])
    x = int(r[1])*1024+int(r[2])

    # New directory name
    nd = os.path.join(outdir,z,str(x))
    try:
        os.makedirs(nd)
    except OSError as err:
        if err.errno == errno.EEXIST:
            pass
        else:
            raise

    y_ = int(r[3])*1024
    for fn in files:
        base, ext = os.path.splitext(fn)
        y = y_+int(base)
        op = os.path.join(root,fn)
        # New file and directory name
        np = os.path.join(nd,str(y)+ext)
        print op, np
        copyfile(op,np)


