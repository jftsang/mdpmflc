import io
from math import sqrt
import numpy as np
import os
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, ImageMagickWriter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from mdpmflc import DPMDIR
from mdpmflc.utils.read_data_file import read_data_file


def create_animation_old(sername, simname, maxframes, samplesize=50000):
    fig = plt.Figure(figsize=(14, 6))
    ax = fig.add_subplot(1,1,1)
    path_collection = ax.scatter([], [], s=[], c=[])

    def init():
        path_collection.set_offsets([])
        return path_collection,
    def animate(ind):
        data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
        print(data_fn)
        dimensions, headline, time, particles = read_data_file(data_fn)
        if samplesize:
            try:
                particles = random.sample(particles, samplesize)
            except ValueError:
                pass
        ax.set_xlim((headline[2], headline[5]))
        ax.set_ylim((headline[3], headline[6]))
        pts = [[p[0], p[1]] for p in particles]
        path_collection.set_offsets(pts)
        path_collection.set_sizes([sqrt(p[6]) for p in particles])
        path_collection.set_array([p[13] for p in particles])
        return path_collection,

    anim = FuncAnimation(fig, animate, init_func=init,
                                   frames=maxframes, interval=20, blit=True)

    return anim

class AnimatedScatter(object):
    """An animated scatter plot using matplotlib.animations.FuncAnimation."""
    # https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot
    def __init__(self, sername, simname, maxframes, samplesize):
        self.sername = sername
        self.simname = simname
        self.samplesize = samplesize
        # self.stream = self.data_stream()

        # Setup the figure and axes...
        self.fig = plt.Figure(figsize=(14,6))
        self.ax = self.fig.add_subplot(1,1,1)
        # Then setup FuncAnimation.
        self.ani = FuncAnimation(self.fig, self.update, interval=5,
                                          frames=maxframes,
                                          init_func=self.setup_plot, blit=True)

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y, s, c = [], [], [], []
        self.scat = self.ax.scatter(x, y, c=c, s=s, vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")
        # self.ax.axis([-10, 10, -10, 10])
        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def update(self, ind):
        """Update the scatter plot."""
        # data = next(self.stream)
        data_fn = os.path.join(DPMDIR, self.sername, self.simname, f"{self.simname}.data.{ind}")
        print(data_fn)
        dimensions, headline, time, particles = read_data_file(data_fn)
        self.ax.set_xlim((headline[2], headline[5]))
        self.ax.set_ylim((headline[3], headline[6]))

        # Set x and y data...
        offsets = [[p[0], p[1]] for p in particles]
        xs = [p[0] for p in particles]
        ys = [p[1] for p in particles]
        radii = [sqrt(p[6]) for p in particles] # TODO wrong way?
        colors = [p[13] for p in particles]
        # self.scat.set_offsets(offsets)
        # Set sizes...
        # self.scat.set_sizes(radii)
        # Set colors..
        # self.scat.set_array(colors)
        self.scat = self.ax.scatter(xs, ys, s=radii, c=colors)

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,


def create_animation(sername, simname, maxframes, samplesize=50000):
    a = AnimatedScatter(sername, simname, maxframes, samplesize)
    return a.ani
