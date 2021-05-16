"""Endpoints that serve plots, as PNG files."""
import logging
import os

import moviepy.editor as mp

import flask
from flask import Response

from mdpmflc.controller.results.plots import need_to_regenerate, MIMETYPE

# https://stackoverflow.com/a/50728936/12695048
# from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
# https://matplotlib.org/gallery/animation/dynamic_image2.html
# import matplotlib.animation as animation

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvas, FigureCanvasAgg

from mdpmflc import CACHEDIR, app
from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.graphics_cg import plot_depth

logging.getLogger().setLevel(logging.INFO)

@app.route("/plots/<sername>/<simname>/<ind>/depth")
def showdepthplot_fig(sername, simname, ind):
    sim = Simulation(sername, simname)

    data_fn = sim.data_fn(ind)

    form = flask.request.values.get("form")
    if form is None:
        form = "png"
    depthplot_fn = os.path.join(
        CACHEDIR, "graphics", sername, simname, f"{simname.replace('data', 'depth')}.{ind}.{form}"
    )

    if (flask.request.values.get("nocache")
        or need_to_regenerate(depthplot_fn, [data_fn])):
        logging.info("Generating a new image")
        os.makedirs(os.path.dirname(depthplot_fn), exist_ok=True)

        fig_width = flask.request.values.get("fig_width")
        fig_width = float(fig_width) if fig_width else 7
        fig_height = flask.request.values.get("fig_height")
        fig_height = float(fig_height) if fig_height else None

        fig = plot_depth(
            data_fn, fig_width=fig_width, fig_height=fig_height
        )
        # canvas = FigureCanvas(fig)
        # print(dir(canvas))
        if form in ["png", "svg", "pdf"]:
            fig.savefig(depthplot_fn, format=form)
        else:
            raise NotImplementedError
    else:
        logging.info("Serving a cached image")

    with open(depthplot_fn, "rb", buffering=0) as depthplot_f:
        return Response(depthplot_f.read(), mimetype=MIMETYPE[form])
