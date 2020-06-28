"""Endpoints that serve plots, as PNG files."""
import io
import os
import numpy as np

import flask
from flask import Response

# https://stackoverflow.com/a/50728936/12695048
# from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
# https://matplotlib.org/gallery/animation/dynamic_image2.html
# import matplotlib.animation as animation

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, ImageMagickWriter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from mdpmflc import DPMDIR, app
from mdpmflc.utils.simulation import get_dt
from mdpmflc.utils.graphics import create_data_figure, create_ene_figure


@app.route("/results/<sername>/<simname>/<ind>/plot/png")
def showdataplot_png(sername, simname, ind):
    """A plot of a .data file, in PNG format."""
    data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")

    fig = create_data_figure(data_fn, vels=get_dt(sername, simname), samplesize=None)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/results/<sername>/<simname>/plotene/")
def showeneplot_png(sername, simname):
    """A plot of a .ene file, in PNG format."""
    ene_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.ene")

    print(ene_fn)
    fig = create_ene_figure(ene_fn)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/anim")
def anim():

    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1, 1)
        return ln,

    def update(frame):
        xdata.append(frame)
        ydata.append(np.sin(frame))
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                        init_func=init, blit=True)
    ani.save("static/anim.mp4")

    return flask.url_for("static", filename="anim.mp4")
