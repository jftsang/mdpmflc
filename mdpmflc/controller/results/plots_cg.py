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
from matplotlib.backends.backend_agg import FigureCanvas, FigureCanvasAgg

from mdpmflc import CACHEDIR, app
from mdpmflc.controller.results.plots import need_to_regenerate, MIMETYPE
from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.graphics_cg import plot_depth, plot_cg_field, plot_all_cg_fields

logging.getLogger().setLevel(logging.INFO)

@app.route("/plots/<sername>/<simname>/<ind>/depth")
def showdepthplot_fig(sername, simname, ind):
    sim = Simulation(sername, simname)

    data_fn = sim.data_fn(ind)

    form = flask.request.values.get("form")
    if form is None:
        form = "png"

    plot_fn = os.path.join(
        CACHEDIR, "graphics", sername, simname,
        ".".join([simname, "depth", ind, form])
    )
    logging.info(plot_fn)

    if (flask.request.values.get("nocache")
        or need_to_regenerate(plot_fn, [data_fn])):
        logging.info("Generating a new image")
        os.makedirs(os.path.dirname(plot_fn), exist_ok=True)

        fig_width = flask.request.values.get("fig_width")
        fig_width = float(fig_width) if fig_width else 7
        fig_height = flask.request.values.get("fig_height")
        fig_height = float(fig_height) if fig_height else None
        colormin = flask.request.values.get("colormin")
        colormin = float(colormin) if colormin else None
        colormax = flask.request.values.get("colormax")
        colormax = float(colormax) if colormax else None

        fig = plot_depth(
            data_fn, fig_width=fig_width, fig_height=fig_height,
            colormin=colormin, colormax=colormax
        )

        if form in ["png", "svg", "pdf"]:
            fig.savefig(plot_fn, format=form)
        else:
            raise NotImplementedError
    else:
        logging.info("Serving a cached image")

    with open(plot_fn, "rb", buffering=0) as plot_f:
        return Response(plot_f.read(), mimetype=MIMETYPE[form])


@app.route("/plots/<sername>/<simname>/<ind>/<field>")
def showcgplot_fig(sername, simname, ind, field):
    if field not in {"depth", "rho", "px", "py", "u", "v"}:
        return ""

    sim = Simulation(sername, simname)

    data_fn = sim.data_fn(ind)

    form = flask.request.values.get("form")
    if form is None:
        form = "png"
    if form not in ["png", "svg", "pdf"]:
        raise NotImplementedError

    plot_fn = os.path.join(
        CACHEDIR, "graphics", sername, simname,
        ".".join([simname, field, ind, form])
    )
    logging.info(plot_fn)

    if (flask.request.values.get("nocache")
        or need_to_regenerate(plot_fn, [data_fn])):
        os.makedirs(os.path.dirname(plot_fn), exist_ok=True)

        fig_width = flask.request.values.get("fig_width")
        fig_width = float(fig_width) if fig_width else 7
        fig_height = flask.request.values.get("fig_height")
        fig_height = float(fig_height) if fig_height else None
        colormin = flask.request.values.get("colormin")
        colormin = float(colormin) if colormin else None
        colormax = flask.request.values.get("colormax")
        colormax = float(colormax) if colormax else None

        logging.info("Generating new CG plots")
        cgfigs = plot_all_cg_fields(data_fn, kernel_width=0.4,
            fig_width=fig_width,
            fig_height=fig_height,
            colormin=colormin,
            colormax=colormax
        )

        for field in cgfigs:
            fn = os.path.join(
                CACHEDIR, "graphics", sername, simname,
                ".".join([simname, field, ind, form])
            )
            logging.info(f"Saving an image to {fn}")
            cgfigs[field].savefig(fn, format=form)

    else:
        logging.info("Serving a cached image")

    with open(plot_fn, "rb", buffering=0) as plot_f:
        return Response(plot_f.read(), mimetype=MIMETYPE[form])
