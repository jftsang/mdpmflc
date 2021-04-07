from math import sqrt
import os
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, ImageMagickWriter
import numpy as np

from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.read_file import read_data_file


def create_animation_old(sername, simname, maxframes, samplesize=50000):
    fig = plt.Figure(figsize=(14, 6))
    ax = fig.add_subplot(1,1,1)
    path_collection = ax.scatter([], [], s=[], c=[])

    def init():
        path_collection.set_offsets([])
        return path_collection,

    def animate(ind):
        sim = Simulation(sername, simname)
        data_fn = sim.data_fn(ind)
        data_df, dimensions, headline = read_data_file(data_fn)
        num, time, xmin, ymin, zmin, xmax, ymax, zmax = headline
        if samplesize:
            try:
                data_df = data_df.sample(n=samplesize)
            except ValueError:
                pass

        ax.set_xlim([xmin, xmax])
        ax.set_ylim([ymin, ymax])
        pts = [(p.x, p.y) for p in data_df.itertuples()]
        path_collection.set_offsets(pts)
        path_collection.set_sizes(np.sqrt(data_df.r))
        path_collection.set_array(data_df.sp)
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
        self.sim = Simulation(sername, simname)
        self.samplesize = samplesize
        # self.stream = self.data_stream()

        # Setup the figure and axes...
        self.fig = plt.Figure(figsize=(12, 6))
        self.ax = self.fig.add_subplot(1,1,1)
        # Then setup FuncAnimation.
        self.ani = FuncAnimation(
            self.fig, self.update, interval=5,
            frames=maxframes,
            init_func=self.setup_plot,
            blit=True
        )

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
        data_fn = self.sim.data_fn(ind)
        print(ind)
        print(data_fn)
        data_df, dimensions, headline = read_data_file(data_fn)
        num, time, xmin, ymin, zmin, xmax, ymax, zmax = headline
        self.ax.set_xlim((xmin, xmax))
        self.ax.set_ylim((ymin, ymax))

        self.scat = self.ax.scatter(
            data_df.x, data_df.y, s=np.sqrt(data_df.r),
            c=data_df.sp,
            cmap=plt.get_cmap("viridis", 3),
            vmin=0, vmax=2
        )

        # We need to return the updated artist for FuncAnimation to draw..
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,


def create_animation(sername, simname, maxframes, samplesize=50000):
    a = AnimatedScatter(sername, simname, maxframes, samplesize)
    return a.ani
