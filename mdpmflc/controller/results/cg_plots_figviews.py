"""Endpoints that serve plots, as PNG files."""
import logging
import os

import moviepy.editor as mp

import flask
from flask import Response, Blueprint

# https://stackoverflow.com/a/50728936/12695048
# from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
# https://matplotlib.org/gallery/animation/dynamic_image2.html
# import matplotlib.animation as animation

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from mdpmflc import CACHEDIR
from mdpmflc.controller.results.plots_figviews import need_to_regenerate, MIMETYPE
from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.graphics_cg import plot_depth, plot_cg_field

logging.getLogger().setLevel(logging.INFO)


cg_plots_figviews = Blueprint('cg_plots_figviews', __name__, )


@cg_plots_figviews.route("/<sername>/<simname>/<ind>/<field>")
def cg_figure_view(sername, simname, ind, field):
    if field not in {"depth", "rho", "px", "py", "u", "v"}:
        raise NotImplementedError

    sim = Simulation(sername, simname)

    data_fn = sim.data_fn(ind)

    form = flask.request.values.get("form")
    if form is None:
        form = "png"
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

        if field == "depth":
            fig = plot_depth(
                data_fn, fig_width=fig_width, fig_height=fig_height,
                colormin=colormin, colormax=colormax
            )
        else:
            fig = plot_cg_field(data_fn, field, kernel_width=0.4,
                    fig_width=fig_width, fig_height=fig_height,
                    colormin=colormin, colormax=colormax
                    )
        # canvas = FigureCanvas(fig)
        # print(dir(canvas))
        if form in ["png", "svg", "pdf"]:
            fig.savefig(plot_fn, format=form)
        else:
            raise NotImplementedError
    else:
        logging.info("Serving a cached image")

    with open(plot_fn, "rb", buffering=0) as plot_f:
        return Response(plot_f.read(), mimetype=MIMETYPE[form])
