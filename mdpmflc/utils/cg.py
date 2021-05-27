import os
import numpy as np
import pandas as pd

from mdpmflc.utils.decorators import timed

@np.vectorize
def kernel(r, kernel_width):
    if r <= kernel_width:
        return (kernel_width**2 - r**2)**2 * 3 / (np.pi * kernel_width**6)
    else:
        return 0


@np.vectorize
def kernel3d(r, kernel_width):
    if r <= kernel_width:
        return 105 / (32 * np.pi * kernel_width**7) * (kernel_width**2 - r**2)**2
    else:
        return 0


@np.vectorize
def dist(x0, y0, x1, y1):
    return np.sqrt((x1 - x0)**2 + (y1 - y0)**2)


@np.vectorize
def dist3d(x0, y0, z0, x1, y1, z1):
    return np.sqrt((x1 - x0)**2 + (y1 - y0)**2 + (z1 - z0)**2)


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

cg_data = timed("coarse-graining")(cg_data)


def cg_general(df, x, y, kernel_width):
    """Calculate the coarse-grained field q(x,y) from value qis at
    positions (xis, yis) in the dataframe.

    Parameters:
        df: A dataframe with columns x, y and q.
        x, y: Coordinates of the point of interest. May be numpy
              arrays (use np.meshgrid).
        kernel_width: The coarse-graining kernel width to use.

    Returns:
        q: The field at the point (or a numpy array).
    """
    if 'q' not in df.columns:
        raise ValueError("The dataframe should contain the column 'q'")

    df2 = df[(x - kernel_width < df.x) & (df.x < x + kernel_width)
            & (y - kernel_width < df.y) & (df.y < y + kernel_width)]
#    df2 = df[mask(df.x, df.y, x, y, kernel_width, kernel_width)]
    if df2.shape[0] == 0:
        return 0
    else:
        dists = dist(x, y, df2.x, df2.y)
        kers = kernel(dists, kernel_width)
        return np.sum(kers * df2.q)

cg_general = np.vectorize(cg_general)
cg_general.excluded.add(0)
cg_general.excluded.add(3)

cg_general = timed("coarse-graining")(cg_general)


def cg_data3d(df, x, y, z, kernel_width):
    df2 = df[(x - kernel_width < df.x) & (df.x < x + kernel_width)
            & (y - kernel_width < df.y) & (df.y < y + kernel_width)
            & (z - kernel_width < df.z) & (df.z < z + kernel_width)
            ]
    if df2.shape[0] == 0:
        rho = px = py = pz = 0.0
    else:
        dists = dist3d(x, y, z, df2.x, df2.y, df2.z)
        kers = kernel3d(dists, kernel_width)
        rho = np.sum(kers * np.pi * df2.r ** 2)
        px = np.sum(kers * np.pi * df2.r ** 2 * df2.u)
        py = np.sum(kers * np.pi * df2.r ** 2 * df2.v)
        pz = np.sum(kers * np.pi * df2.r ** 2 * df2.w)

    return rho, px, py, pz

cg_data3d = np.vectorize(cg_data3d)
cg_data3d.excluded.add(0)
cg_data3d.excluded.add(4)


def cg_general3d(df, x, y, z, kernel_width):
    """Calculate the coarse-grained field q(x,y, z) from value qis at
    positions (xis, yis, zis) in the dataframe.

    Parameters:
        df: A dataframe with columns x, y and q.
        x, y, z: Coordinates of the point of interest. May be numpy
                 arrays (use np.meshgrid).
        kernel_width: The coarse-graining kernel width to use.

    Returns:
        q: The field at the point (or a numpy array).
    """
    if 'q' not in df.columns:
        raise ValueError("The dataframe should contain the column 'q'")

    df2 = df[
        (x - kernel_width < df.x) & (df.x < x + kernel_width)
        & (y - kernel_width < df.y) & (df.y < y + kernel_width)
        & (z - kernel_width < df.z) & (df.z < z + kernel_width)
    ]
    if df2.shape[0] == 0:
        return 0
    else:
        dists = dist3d(x, y, z, df2.x, df2.y, df2.z)
        kers = kernel3d(dists, kernel_width)
        return np.sum(kers * df2.q)

cg_general3d = np.vectorize(cg_general3d)
cg_general3d.excluded.add(0)
cg_general3d.excluded.add(4)

cg_general3d = timed("coarse-graining")(cg_general3d)


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


def depth(df, x, y, kernel_width, period_y=None, percentile=95):
    if period_y:
        df2 = df[
            (x - kernel_width < df.x) & (df.x < x + kernel_width)
            & (
                ((y - kernel_width < df.y) & (df.y < y + kernel_width))
                | ((y - kernel_width < df.y - period_y) & (df.y - period_y < y + kernel_width))
                | ((y - kernel_width < df.y + period_y) & (df.y + period_y < y + kernel_width))
            )
        ]
    else:
        df2 = df[(x - kernel_width < df.x) & (df.x < x + kernel_width)
                & (y - kernel_width < df.y) & (df.y < y + kernel_width)]

    if df2.shape[0]:
        return np.percentile(df2.z, percentile)
    else:
        return 0

depth = np.vectorize(depth)
depth.excluded.add(0)
depth.excluded.add(4)
depth.excluded.add(5)
