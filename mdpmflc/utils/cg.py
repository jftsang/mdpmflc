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
    df2 = df[(x - kernel_width < df.x) & (df.x < x + kernel_width)
            & (y - kernel_width < df.y) & (df.y < y + kernel_width)]
    if df2.shape[0] == 0:
        rho = px = py = 0.0
    else:
        rho = sum(df2.apply(
            lambda p: kernel(dist(x, y, p.x, p.y), kernel_width) * np.pi * p.r**2,
            axis=1
        ))
        px = sum(df2.apply(
            lambda p: kernel(dist(x, y, p.x, p.y), kernel_width) * np.pi * p.r**2 * p.u,
            axis=1
        ))
        py = sum(df2.apply(
            lambda p: kernel(dist(x, y, p.x, p.y), kernel_width) * np.pi * p.r**2 * p.v
            , axis=1
        ))
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
