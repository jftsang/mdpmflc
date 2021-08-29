"""Creating figures that show coarse-grained fields."""
from typing import Dict

from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from mdpmflc.utils.cg import (
    cg_data,
    x_front,
    depth
)
from mdpmflc.utils.decorators import timed
from mdpmflc.utils.read_file import read_data_file


def plot_field(
    xg, yg, field_g,
    fig_width=7, fig_height=None,
    colormin=None, colormax=None
):
    """Plotting of a generic continuum field.

    Arguments:
        colormin, colormax: Range for the colorbar

    Returns:
        fig: An instance of plt.Figure
    """
    if fig_height is None:
        xmin = min(xg.flatten())
        xmax = max(xg.flatten())
        ymin = min(yg.flatten())
        ymax = max(yg.flatten())
        fig_height = (ymax-ymin)/(xmax-xmin)*fig_width - 0.0

    fig = Figure(figsize=(fig_width, fig_height))
    ax = fig.add_subplot(111)

    if colormin is None:
        # colormin = 0
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
    **kwargs
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
    num, time, xmin, ymin, zmin, xmax, ymax, zmax = headline
    xmax = 40

    xs, ys = np.linspace(xmin, xmax), np.linspace(ymin, ymax)
    xg, yg = np.meshgrid(xs, ys)

    depth_g = depth(
        data_df, xg, yg, kernel_width, period_y=(ymax-ymin),
        percentile=percentile
    )

    return plot_field(xg, yg, depth_g, **kwargs)


@timed("creating plot for the field {field}")
def plot_cg_field(data_fn, field, kernel_width=0.4, **kwargs):
    """Produce a plot of a field from a .data file.

    Arguments:
        data_fn:
        field: One of 'rho', 'px', 'py', 'u', or 'v'
        kernel_width: Radius of coarse-graining kernels

    Returns:
        fig: An instance of plt.Figure
    """
    data_df, dimensions, headline = read_data_file(data_fn)
    num, time, xmin, ymin, zmin, xmax, ymax, zmax = headline
    xmax = 40

    xs, ys = np.linspace(xmin, xmax), np.linspace(ymin, ymax)
    xg, yg = np.meshgrid(xs, ys)

    rhog, pxg, pyg = cg_data(data_df, xg, yg, kernel_width=kernel_width)

    if field == "rho":
        field_g = rhog
    elif field == "px":
        field_g = pxg
    elif field == "py":
        field_g = pyg
    elif field == "u":
        field_g = pxg / rhog
    elif field == "v":
        field_g = pyg / rhog
    else:
        raise NotImplementedError
    return plot_field(xg, yg, field_g, **kwargs)


@timed("creating plots for all cg fields of {data_fn}")
def plot_all_cg_fields(data_fn, kernel_width=0.4, **kwargs) -> Dict[str, Figure]:
    """As above, but produce plots of all fields.

    Arguments:
        data_fn:
        kernel_width: Radius of coarse-graining kernels

    Returns:
        figs: A dictionary of figures
    """
    data_df, dimensions, headline = read_data_file(data_fn)
    num, time, xmin, ymin, zmin, xmax, ymax, zmax = headline
    xmax = 40

    # xs, ys = np.linspace(xmin, xmax, 100), np.linspace(ymin, ymax, 100)
    xs, ys = np.linspace(xmin, xmax), np.linspace(ymin, ymax)
    xg, yg = np.meshgrid(xs, ys)

    rhog, pxg, pyg = cg_data(data_df, xg, yg, kernel_width=kernel_width)

    return {
        "rho": plot_field(xg, yg, rhog, **kwargs),
        "px": plot_field(xg, yg, pxg, **kwargs),
        "py": plot_field(xg, yg, pyg, **kwargs),
        "u": plot_field(xg, yg, pxg / rhog, **kwargs),
        "v": plot_field(xg, yg, pyg / rhog, **kwargs),
    }
