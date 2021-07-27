"""Endpoints that serve plots, as PNG files."""
import logging
import os

import moviepy.editor as mp

import flask
from flask import Response

# https://stackoverflow.com/a/50728936/12695048
# from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
# https://matplotlib.org/gallery/animation/dynamic_image2.html
# import matplotlib.animation as animation

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, ImageMagickWriter
from matplotlib.backends.backend_agg import FigureCanvas, FigureCanvasAgg

from mdpmflc import CACHEDIR, app
from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.graphics import create_data_figure, create_ene_figure
from mdpmflc.utils.graphics_cg import plot_depth
from mdpmflc.utils.anims import create_animation

logging.getLogger().setLevel(logging.INFO)

MIMETYPE = {
    'png': 'image/png',
    'svg': 'image/svg',
    'pdf': 'application/pdf'
}

def need_to_regenerate(target, sources):
    if not os.path.isfile(target):
        return True
    if os.path.getsize(target) == 0:
        return True
    if any([os.path.getmtime(target) < os.path.getmtime(s) for s in sources]):
        return True
    return False


@app.route("/plots/<sername>/<simname>/<ind>/data")
def showdataplot_fig(sername, simname, ind):
    """A plot of a .data file, in PNG format by default."""
    sim = Simulation(sername, simname)
    form = flask.request.values.get("form")
    if form is None:
        form = "png"

    data_fn = sim.data_fn(ind)
    dataplot_fn = os.path.join(
        CACHEDIR, "graphics", sername, simname, f"{simname}.data.{ind}.{form}"
    )

    if (flask.request.values.get("nocache")
        or need_to_regenerate(dataplot_fn, [data_fn])):
        logging.info("Generating a new image")
        os.makedirs(os.path.dirname(dataplot_fn), exist_ok=True)

        samplesize = flask.request.values.get("samplesize")
        samplesize = float(samplesize) if samplesize else 20000

        fig_width = flask.request.values.get("width")
        fig_width = float(fig_width) if fig_width else 7
        fig_height = flask.request.values.get("height")
        fig_height = float(fig_height) if fig_height else None

        fig = create_data_figure(
            data_fn, samplesize=samplesize,
            fig_width=fig_width,
            fig_height=fig_height,
        )
        # canvas = FigureCanvas(fig)
        # print(dir(canvas))
        if form in ["png", "svg", "pdf"]:
            fig.savefig(dataplot_fn, format=form)
        else:
            raise NotImplementedError
    else:
        logging.info("Serving a cached image")

    with open(dataplot_fn, "rb", buffering=0) as dataplot_f:
        return Response(dataplot_f.read(), mimetype=MIMETYPE[form])


@app.route("/plots/<sername>/<simname>/ene")
def showeneplot_png(sername, simname):
    """A plot of a .ene file, in PNG format."""
    sim = Simulation(sername, simname)
    ene_fn = sim.ene_fn()
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


@app.route("/plots/<sername>/<simname>/animate")
def anim(sername, simname):
    sim = Simulation(sername, simname)
    # https://github.com/matplotlib/matplotlib/issues/16965
    anim_fn = os.path.join(CACHEDIR, "graphics", sername, simname, f"{simname}.gif")
    os.makedirs(os.path.dirname(anim_fn), exist_ok=True)
    base_fn = sim.data_fn()

    if flask.request.values.get("maxind"):
        max_data_index = int(flask.request.values.get("maxind"))
    else:
        max_data_index = sim.status()['dataFileCounter']

    datafiles = [f"{base_fn}.{ind}" for ind in range(max_data_index)]
    if (flask.request.values.get("nocache")
        or need_to_regenerate(anim_fn, datafiles)):
        ani = create_animation(
            sername, simname, maxframes=max_data_index, samplesize=3000
        )
        ani.save(anim_fn, writer="imagemagick")
        # ani.save(anim_fn, writer="ffmpeg")

    if flask.request.values.get("format") == "webm":
        clip = mp.VideoFileClip(anim_fn)
        webm_fn = f"{anim_fn}.webm"
        clip.write_videofile(webm_fn)

        with open(webm_fn, "rb") as webm_f:
            return Response(webm_f.read(), mimetype="video/webm")
    else:
        with open(anim_fn, "rb") as anim_f:
            return Response(anim_f.read(), mimetype="image/gif")
