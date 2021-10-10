"""Endpoints that serve plots, as PNG files."""
import logging
import os
from tempfile import NamedTemporaryFile, TemporaryDirectory

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
from mdpmflc.controller.results.plots_figviews import MIMETYPE, floatify
from mdpmflc.models import Simulation
from mdpmflc.utils.decorators import timed
from mdpmflc.utils.graphics_cg import plot_depth, plot_all_cg_fields

logging.getLogger().setLevel(logging.INFO)


cg_plots_figviews = Blueprint('cg_plots_figviews', __name__, )


@cg_plots_figviews.route("/<sername>/<simname>/<ind>/depth")
@timed("depth_plot_figview for {simname}:{ind}")
def depth_plot_figview(sername, simname, ind):
    sim = Simulation(sername, simname)

    data_fn = sim.data_fn(ind)

    format = flask.request.values.get("format", default="png")
    if format not in ["png", "svg", "pdf"]:
        raise NotImplementedError

    plot_fn = os.path.join(
        CACHEDIR, "graphics", sername, simname,
        ".".join([simname, "depth", ind, format])
    )
    logging.info(plot_fn)

    logging.info("Generating a new image")
    os.makedirs(os.path.dirname(plot_fn), exist_ok=True)

    fig = plot_depth(data_fn, **floatify(flask.request.values))
    with NamedTemporaryFile(suffix="." + format) as ntf:
        fig.savefig(ntf, format=format)
        ntf.seek(0)
        return Response(ntf.read(), mimetype=MIMETYPE[format])


@cg_plots_figviews.route("/<sername>/<simname>/<ind>/<field>")
@timed("cg_plot_figview for {simname}:{ind}, field {field}")
def cg_plot_figview(sername, simname, ind, field):
    if field not in {"depth", "rho", "px", "py", "u", "v"}:
        raise NotImplementedError

    format = flask.request.values.get("format", "png")
    if format not in ["png", "svg", "pdf"]:
        raise NotImplementedError


    sim = Simulation(sername, simname)

    data_fn = sim.data_fn(ind)


    logging.info("Generating new CG plots")
    cgfigs = plot_all_cg_fields(
        data_fn, kernel_width=0.4, **floatify(flask.request.values)
    )

    with TemporaryDirectory() as td:
        fn = os.path.join(
            td, ".".join([simname, field, ind, format])
        )
        cgfigs[field].savefig(fn, format=format)

        with open(fn, "rb", buffering=0) as plot_f:
            return Response(plot_f.read(), mimetype=MIMETYPE[format])
