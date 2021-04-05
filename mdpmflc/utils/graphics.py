from math import sqrt
import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
from matplotlib.animation import FuncAnimation, ImageMagickWriter
# https://matplotlib.org/gallery/animation/dynamic_image2.html
import matplotlib.animation as animation

from mdpmflc.utils.read_file import read_data_file, read_ene_file


def create_data_figure(data_fn, vels=None, samplesize=50000):
    """Plots the data from a .data file. Returns the figure as a
    plt.Figure object.

    If samplesize is given, it specifies the number of points to be
    plotted. If it is None, or if it is smaller than the number of
    particles, then all particles are plotted.
    """
    fig = Figure(figsize=(14, 6))
    ax = fig.add_subplot(1, 1, 1)

    dimensions, headline, time, particles = read_data_file(data_fn)

    if samplesize:
        try:
            particles = random.sample(particles, samplesize)
        except ValueError:
            pass

    xs = [p[0] for p in particles]
    ys = [p[1] for p in particles]
    if dimensions == 2:
        rs = [p[4] for p in particles]
        sps = [p[7] for p in particles]
    if dimensions == 3:
        rs = [p[6] for p in particles]
        sps = [p[13] for p in particles]

    # ax.scatter(xs, ys, marker='.', s=1, c=sps)
    # ax.scatter(xs, ys, marker='o', s=rs, c=sps, cmap='hsv')
    # ax.scatter(xs, ys, marker='.', s=rs, c=sps)
    # https://stackoverflow.com/questions/33094509/correct-sizing-of-markers-in-scatter-plot-to-a-radius-r-in-matplotlib#33095224
    # https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size#14860958
    ax.scatter(xs, ys, s=[sqrt(r) for r in rs], c=sps)

    if vels:
        if dimensions == 2:
            us = [p[2] for p in particles]
            vs = [p[3] for p in particles]
        if dimensions == 3:
            us = [p[3] for p in particles]
            vs = [p[4] for p in particles]

        for i in range(len(xs)):
            ax.arrow(xs[i], ys[i], us[i] * vels, vs[i] * vels)

    if dimensions == 2:
        ax.set_xlim((headline[2], headline[4]))
        ax.set_ylim((headline[3], headline[5]))
    if dimensions == 3:
        ax.set_xlim((headline[2], headline[5]))
        ax.set_ylim((headline[3], headline[6]))
    ax.set_aspect('equal')

    ax.grid()
    return fig


def create_ene_figure(ene_fn):
    """Plot the information in an .ene file."""
    ene_df = read_ene_file(ene_fn)

    fig = Figure(figsize=(14,6))
    axs = fig.subplots(2, 2)
    axs[0,0].plot(ene_df.time, ene_df.gravitEnergy, 'g',
                ene_df.time, ene_df.traKineticEnergy, 'b',
                ene_df.time, ene_df.elasticEnergy, 'r')
    axs[0,0].legend(['gravitEnergy', 'traKineticEnergy', 'elasticEnergy'])
    axs[0,0].grid()

    axs[0,1].plot(ene_df.time, ene_df.traKineticEnergy, 'b',
                ene_df.time, ene_df.rotKineticEnergy, 'c',
                ene_df.time, ene_df.elasticEnergy, 'r')
    axs[0,1].set_xlabel('time')
    axs[0,1].legend(
        ['traKineticEnergy', 'rotKineticEnergy', 'elasticEnergy']
    )
    max_y = max(
        np.percentile(ene_df.traKineticEnergy.array, 95),
        np.percentile(ene_df.rotKineticEnergy.array, 95),
        np.percentile(ene_df.elasticEnergy.array, 95)
    )
    axs[0,1].set_ylim([0, max_y])
    axs[0,1].grid()

    axs[1,0].plot(
        ene_df.time,
        np.sqrt(ene_df.traKineticEnergy / ene_df.gravitEnergy), 'k')
    axs[1,0].set_xlabel('time')
    axs[1,0].set_ylabel('sqrt(TKE/GPE)')
    axs[1,0].grid()

    axs[1,1].plot(
        ene_df.time, ene_df.traKineticEnergy, 'b',
        ene_df.time, ene_df.rotKineticEnergy, 'c',
        ene_df.time, ene_df.elasticEnergy, 'r'
    )
    axs[1,1].set_xlabel('time')
    axs[1,1].set_ylabel('energy')
    axs[1,1].set_yscale('log')
    axs[1,1].legend(
        ['traKineticEnergy', 'rotKineticEnergy', 'elasticEnergy']
    )
    axs[1,1].grid()
    return fig
