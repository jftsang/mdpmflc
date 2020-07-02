"""Endpoints that serve plots, as PNG files."""
import io
import logging
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

from mdpmflc import DPMDIR, CACHEDIR, app
from mdpmflc.utils.simulation import get_dt
from mdpmflc.utils.graphics import create_data_figure, create_ene_figure

logging.getLogger().setLevel(logging.INFO)

def need_to_regenerate(target, sources):
    if not os.path.isfile(target):
        return True
    if os.path.getsize(target) == 0:
        return True
    if any([os.path.getmtime(target) < os.path.getmtime(s) for s in sources]):
        return True
    return False


@app.route("/results/<sername>/<simname>/<ind>/plot/png")
def showdataplot_png(sername, simname, ind):
    """A plot of a .data file, in PNG format."""
    data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dataplot_fn = os.path.join(CACHEDIR, "graphics", sername, simname, f"{simname}.data.{ind}.png")

    if (flask.request.values.get("nocache")
        or need_to_regenerate(dataplot_fn, [data_fn])):
        logging.info("Generating a new image")
        os.makedirs(os.path.dirname(dataplot_fn), exist_ok=True)
        fig = create_data_figure(data_fn, samplesize=50000)
        FigureCanvas(fig).print_png(dataplot_fn)
    else:
        logging.info("Serving a cached image")

    with open(dataplot_fn, "rb", buffering=0) as dataplot_f:
        return Response(dataplot_f.read(), mimetype='image/png')



@app.route("/results/<sername>/<simname>/plotene/")
def showeneplot_png(sername, simname):
    """A plot of a .ene file, in PNG format."""
    ene_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.ene")
    eneplot_fn = os.path.join(CACHEDIR, "graphics", sername, simname, f"{simname}.ene.png")

    if (flask.request.values.get("nocache")
        or need_to_regenerate(eneplot_fn, [ene_fn])):
        logging.info("Generating a new image")
        os.makedirs(os.path.dirname(eneplot_fn), exist_ok=True)
        fig = create_ene_figure(ene_fn)
        FigureCanvas(fig).print_png(eneplot_fn)
    else:
        logging.info("Serving a cached image")

    with open(eneplot_fn, "rb") as eneplot_f:
        return Response(eneplot_f.read(), mimetype='image/png')


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
    # ani.save(os.path.join(CACHEDIR, "graphics", "anim.mp4")
    ani.save("static/anim.mp4")

    return flask.url_for("static", filename="anim.mp4")
