import os

import flask
from flask import render_template, Blueprint, send_file
from flask_breadcrumbs import register_breadcrumb

from mdpmflc.config import DPMDIR, DPMDRIVERS
from mdpmflc.models import Driver
from mdpmflc.utils.listings import get_available_series

static_views = Blueprint('static_views', __name__, )


@static_views.route("/")
@register_breadcrumb(static_views, '.', 'Index')
def main_page():
    drivers = Driver.query.all()
    return render_template("mainpage.html",
                           hostname=flask.request.host,
                           DPMDIR=DPMDIR,
                           available_series=get_available_series(),
                           available_drivers=drivers)


@static_views.route("/help")
def help_page():
    """A page that shows help."""
    src_fn = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)), "..", "static", "MdpmflcTutorial.cpp")
    src_f = open(src_fn, "r")
    example_driver_src = src_f.read()

    ex_fn = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)), "..", "static", "mdpmflc_example.config")
    ex_f = open(ex_fn, "r")
    example_config = ex_f.read()

    return render_template("help.html",
                           example_driver_src=example_driver_src,
                           example_config=example_config)


@static_views.route("/favicon.ico")
def favicon():
    return send_file("static/favicon.ico")
