import random

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
from matplotlib.animation import FuncAnimation, ImageMagickWriter
# https://matplotlib.org/gallery/animation/dynamic_image2.html
import matplotlib.animation as animation

from mdpmflc.utils.read_data_file import read_data_file


def create_data_figure(data_fn, vels=0.1, samplesize=None):
    """Plots the data from a .data file."""
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
        rs = [p[5] for p in particles]
        sps = [p[8] for p in particles]
    if dimensions == 3:
        rs = [p[7] for p in particles]
        sps = [p[13] for p in particles]

    # ax.scatter(xs, ys, marker='.', s=1, c=sps)
    ax.scatter(xs, ys, marker='o', c=sps)
    # https://stackoverflow.com/questions/33094509/correct-sizing-of-markers-in-scatter-plot-to-a-radius-r-in-matplotlib#33095224
    # https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size#14860958
    # ax.scatter(xs, ys, s=[sqrt(r) for r in rs])

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


#def lagrangian_trace(sername, simname):
#    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
#    dimensions, headline, time, particles = read_data_file(dat_fn)
