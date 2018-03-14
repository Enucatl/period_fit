from __future__ import division, print_function
import click
import glob
import os
import numpy as np
from PIL import Image
from cogent.maths.period import dft

@click.command()
@click.argument("scan_range", type=float)
@click.argument("folder", type=click.Path(exists=True))
def main(scan_range, folder):
    filenames = sorted(
        glob.glob(
            os.path.join(
                folder, "*.tif")
        )
    )
    images = [Image.open(x) for x in filenames]
    arrays = [np.array(x) for x in images]
    a = np.dstack(arrays)
    pwr, period = dft(a)
    pwr = abs(pwr)
    print(pwr.shape, period.shape)



if __name__ == "__main__":
    main()
