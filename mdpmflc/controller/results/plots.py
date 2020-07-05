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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from mdpmflc import DPMDIR, CACHEDIR, app
from mdpmflc.utils.simulation import get_max_indices
from mdpmflc.utils.graphics import create_data_figure, create_ene_figure
from mdpmflc.utils.anims import create_animation

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


@app.route("/results/<sername>/<simname>/animate")
def anim(sername, simname):
    # https://github.com/matplotlib/matplotlib/issues/16965
    anim_fn = os.path.join(CACHEDIR, "graphics", sername, simname, f"{simname}.gif")
    os.makedirs(os.path.dirname(anim_fn), exist_ok=True)
    base_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data")

    if flask.request.values.get("maxind"):
        max_data_index = int(flask.request.values.get("maxind"))
    else:
        _, max_data_index, _ = get_max_indices(sername, simname)

    datafiles = [f"{base_fn}.{ind}" for ind in range(max_data_index)]
    print(datafiles)
    if (flask.request.values.get("nocache")
        or need_to_regenerate(anim_fn, datafiles)):
        ani = create_animation(sername, simname, maxframes=max_data_index, samplesize=3000)
        ani.save(anim_fn, writer="imagemagick")
        # ani.save(anim_fn, writer="ffmpeg")

    clip = mp.VideoFileClip(anim_fn)

    webm_fn = f"{anim_fn}.webm"
    clip.write_videofile(webm_fn)

    with open(webm_fn, "rb") as anim_f:
        # return Response(anim_f.read(), mimetype="image/gif")
        return Response(anim_f.read(), mimetype="video/webm")
