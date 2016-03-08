#!/usr/bin/env python

import os
import errno
from shutil import copyfile, move
import click

def zoom(z):
    z = int(z)
    z = -(z+2)+19
    return str(z)

extensions = ('.jpg','.png')

@click.command()
@click.argument('indir', type=click.Path(exists=True))
@click.argument('outdir',type=click.Path())
@click.option('--copy/--no-copy','-c',default=False)
@click.option('--verbose','-v',is_flag=True, default=False)
def cli(indir,outdir,copy=False, verbose=False):
    """
    Change files from GMapCatcher format into classic z/x/y format
    """

    # Set the function we will use on files
    op = copyfile if copy else move

    try:
        os.mkdir(outdir)
    except OSError as err:
        pass

    dl = len(indir.split("/"))

    # Tiles start in top-left presumably
    for root, subfolders, files in os.walk(indir):

        files = [f for f in files if f.endswith(extensions)]

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
            paths = (
                os.path.join(root,fn),
                os.path.join(nd,str(y)+ext))

            if verbose: click.echo(*paths)
            op(*paths)

if __name__ == '__main__':
    cli()
