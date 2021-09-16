"""Creating figures that show coarse-grained fields."""
from typing import Dict

import numpy as np
from matplotlib import cm
from matplotlib.figure import Figure

from mdpmflc.utils.cg import cg_data, depth
from mdpmflc.utils.decorators import timed
from mdpmflc.utils.read_file import read_data_file


def plot_field(
    xg, yg, field_g,
    fig_width=7, fig_height=None,
    xmin=None, xmax=None, ymin=None, ymax=None,
    colormin=None, colormax=None
):
    """Plotting of a generic continuum field.

    Arguments:
        colormin, colormax: Range for the colorbar

    Returns:
        fig: An instance of plt.Figure
    """
    if xmin is None:
        xmin = min(xg.flatten())
    if xmax is None:
        xmax = max(xg.flatten())
    if ymin is None:
        ymin = min(yg.flatten())
    if ymax is None:
        ymax = max(yg.flatten())

    if fig_height is None:
        fig_height = (ymax-ymin)/(xmax-xmin)*fig_width - 0.0

    fig = Figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111)

    if colormin is None:
        colormin = np.percentile(field_g.flatten(), 0)
    if colormax is None:
        colormax = np.percentile(field_g.flatten(), 95)

    norm = cm.colors.Normalize(vmin=colormin, vmax=colormax)
    pcm = ax.pcolormesh(xg, yg, field_g, norm=norm, shading='gouraud')
    ax.set_aspect('equal')
    fig.colorbar(pcm, orientation="horizontal")
    return fig


@timed("creating plot of depths of {data_fn}")
def plot_depth(
    data_fn,
    kernel_width=0.4,
    percentile=99,
    fig_width=7, fig_height=None,
    xmin=None, xmax=None, ymin=None, ymax=None,
    nx=50, ny=50,
    **kwargs,
):
    """Produce a plot of the flow depth from a .data file.

    Args:
        data_fn:
        kernel_width: Radius of coarse-graining kernels
        percentile:
        colormin, colormax: Range for the colorbar

    Returns:
        fig: An instance of plt.Figure
    """
    data_df, dimensions, headline = read_data_file(data_fn)
    num, time, xmin_, ymin_, zmin_, xmax_, ymax_, zmax_ = headline
    if xmin is None:
        xmin = xmin_
    if xmax is None:
        xmax = xmax_
    if ymin is None:
        ymin = ymin_
    if ymax is None:
        ymax = ymax_

    xs, ys = np.linspace(xmin, xmax, int(nx)), np.linspace(ymin, ymax, int(ny))
    xg, yg = np.meshgrid(xs, ys)

    depth_g = depth(
        data_df, xg, yg, kernel_width, period_y=(ymax-ymin),
        percentile=percentile
    )

    return plot_field(xg, yg, depth_g, fig_width, fig_height,
                      xmin, xmax, ymin, ymax, **kwargs)


@timed("running plot_all_cg_fields of {data_fn}")
def plot_all_cg_fields(
        data_fn, kernel_width=0.4,
        xmin=None, xmax=None, ymin=None, ymax=None,
        nx=50, ny=50,
        **kwargs,
) -> Dict[str, Figure]:
    """As above, but produce plots of all fields.

    Arguments:
        data_fn:
        kernel_width: Radius of coarse-graining kernels

    Returns:
        figs: A dictionary of figures
    """
    data_df, dimensions, headline = read_data_file(data_fn)
    num, time, xmin_, ymin_, zmin_, xmax_, ymax_, zmax_ = headline
    if xmin is None:
        xmin = xmin_
    if xmax is None:
        xmax = xmax_
    if ymin is None:
        ymin = ymin_
    if ymax is None:
        ymax = ymax_

    xs, ys = np.linspace(xmin, xmax, int(nx)), np.linspace(ymin, ymax, int(ny))
    xg, yg = np.meshgrid(xs, ys)

    rhog, pxg, pyg = cg_data(data_df, xg, yg, kernel_width=kernel_width)

    return {
        "rho": plot_field(xg, yg, rhog, **kwargs),
        "px": plot_field(xg, yg, pxg, **kwargs),
        "py": plot_field(xg, yg, pyg, **kwargs),
        "u": plot_field(xg, yg, pxg / rhog, **kwargs),
        "v": plot_field(xg, yg, pyg / rhog, **kwargs),
    }
