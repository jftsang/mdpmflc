import os
import numpy as np
import pandas as pd


@np.vectorize
def kernel(r, kernel_width):
    if r <= kernel_width:
        return (kernel_width**2 - r**2)**2 * 3 / (np.pi * kernel_width**6)
    else:
        return 0


@np.vectorize
def dist(x0, y0, x1, y1):
    return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)


def cg_data(df, x, y, kernel_width):
    """Calculate the 2D coarse-grained fields at the specified point
    (x, y).

    Parameters:
        df: A dataframe of particles (use read_data_file).
        x, y: Coordinates of the point of interest. May be numpy
              arrays (use np.meshgrid).
        kernel_width: The coarse-graining kernel width to use.

    Returns:
        rho, px, py: The density and momentum fields at the specified
                     position(s). May be numpy arrays.
    """
    # Calculating the distance between points is quite an expensive
    # process, even if vectorized. Therefore, we filter the dataframe
    # before calculating distances and kernels. Note that the filter
    # includes some particles that are more than kernel_width away from
    # the point of interest - these will result in kernel = 0.
    df2 = df[(x - kernel_width < df.x) & (df.x < x + kernel_width)
            & (y - kernel_width < df.y) & (df.y < y + kernel_width)]
    if df2.shape[0] == 0:
        rho = px = py = 0.0
    else:
        dists = dist(x, y, df2.x, df2.y)
        kers = kernel(dists, kernel_width)
        rho = np.sum(kers * np.pi * df2.r ** 2)
        px = np.sum(kers * np.pi * df2.r ** 2 * df2.u)
        py = np.sum(kers * np.pi * df2.r ** 2 * df2.v)

    return rho, px, py

cg_data = np.vectorize(cg_data)
cg_data.excluded.add(0)
cg_data.excluded.add(3)


def x_front(df, y, dy, periodicity=None, percentile=95):
    if periodicity:
        sub_df = df[
            (df.sp == 0)
            & (
                ((y - dy < df.y) & (df.y < y + dy))
                | ((y - dy < df.y - periodicity) & (df.y - periodicity < y + dy))
                | ((y - dy < df.y + periodicity) & (df.y + periodicity < y + dy))
            )
        ]
    else:
        sub_df = df[
            (df.sp == 0) & (y - dy < df.y) & (df.y < y + dy)
        ]
    if sub_df.shape[0]:
        return np.percentile(sub_df.x, percentile)
    else:
        return 0

x_front = np.vectorize(x_front)
x_front.excluded.add(0)
x_front.excluded.add(2)
x_front.excluded.add(3)
x_front.excluded.add(4)
