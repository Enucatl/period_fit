from __future__ import division, print_function
import click
import glob
import os
import numpy as np
import h5py
import scipy.signal as ss
import matplotlib.pyplot as plt


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("--fs", type=float, default=1, help="sampling frequency")
def main(filename, fs):
    with h5py.File(filename, "r") as h5file:
        group = h5file["/entry/data/threshold_0"]
        dataset_names = sorted(list(group.keys()))
        a = np.dstack(group[key] for key in dataset_names)
        print(a.shape)
        f, pxx = ss.periodogram(a, fs)
        print(f.shape)
        print(pxx.shape)
        indices_sorted = np.argsort(np.abs(pxx))[::-1]
        for i in range(1, indices_sorted.shape[-1]):
            indices = indices_sorted[:, :, i]
            periods = 1 / f[indices]
            valid_periods = periods[a[..., 0] > 0]
            valid_periods = valid_periods[valid_periods > 0.5]
            print(i, np.size(valid_periods), np.mean(valid_periods), np.std(valid_periods))
        # plt.ion()
        # plt.show()
        # input("close")


if __name__ == "__main__":
    main()
