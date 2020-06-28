#!/usr/bin/env python3
"""
Flask web interface for controlling MercuryDPM simulations and viewing
their results.

Preparation:
    pip install Flask
    pip install matplotlib

To run:
    export FLASK_APP='mdpmflc.py'
    export FLASK_ENV='development'
    flask run --host=0.0.0.0 --debugger
"""
import flask
from flask import Flask, Response
from flask import render_template

# https://stackoverflow.com/a/50728936/12695048
import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
from matplotlib.animation import FuncAnimation, ImageMagickWriter
# https://matplotlib.org/gallery/animation/dynamic_image2.html
# import matplotlib.animation as animation

# import random
# from math import pi, sqrt
import numpy as np
import os
# import fnmatch

# For starting new simulations
import subprocess

# Diagnosis
# from pprint import pprint, pformat

# Configuration
from . import DPMDIR, SRCDIR, DPMDRIVERS
from . import app

# Utilities
from .utils.read_data_file import read_data_file
from .utils.graphics import create_data_figure
from .utils.simulation import get_dt, get_max_indices
from .utils.listings import get_available_series

# Controllers
from .controller.driver.viewDriver import *
from .controller.results.simulation import *
from .controller.results.listing import *
from .controller.results.plots import *
from .controller.results.raw import *

# Error handlers
from .errorhandlers import not_found


@app.route("/run", methods=["POST"])
def run_a_simulation():
    """Start a simulation."""
    # https://code.luasoftware.com/tutorials/flask/flask-get-request-parameters-get-post-and-json/
    if flask.request.method == "GET":
        raise Exception("Sorry, you should request this page with a POST request")

    if "driver" in flask.request.values:
        driver = flask.request.values.get("driver")
    else:
        raise Exception("driver not given")

    if driver not in DPMDRIVERS:
        raise Exception(f"{driver} is not a recognised driver.")

    if "sername" in flask.request.values:
        sername = flask.request.values.get("sername")
    else:
        raise Exception("sername not given")

    if "simname" in flask.request.values:
        simname = flask.request.values.get("simname")
    else:
        raise Exception("simname not given")

    executable = os.path.join(DPMDIR, driver)
    simdir = os.path.join(DPMDIR, sername, simname)
    try:
        os.mkdir(simdir)
    except PermissionError as e:
        raise e  # TODO
    except FileExistsError as e:
        raise e  # TODO
        # raise e(f"{simdir} already exists")

    # Start the simulation
    stdout_f = open(os.path.join(simdir, f"{simname}.log"), "a")
    stderr_f = open(os.path.join(simdir, f"{simname}.err"), "a")
    subprocess.run([executable, "-name", simname],
                   cwd=simdir,
                   stdout=stdout_f,
                   stderr=stderr_f)

    # return pformat(dir(flask.request.form))
    # return f"Started a run of driver {driver} on series {sername}, simulation name {simname}"
    # return Response(flask.request.get_json(), mimetype="application/json")
    return render_template("successful_start.html",
                           hostname=flask.request.host,
                           driver=driver,
                           sername=sername,
                           simname=simname)


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


### Miscellaneous

@app.route('/')
def mainpage():
    return render_template("mainpage.html",
                           hostname=flask.request.host,
                           DPMDIR=DPMDIR,
                           available_series=get_available_series(),
                           available_drivers=DPMDRIVERS)


@app.route('/style.css')
def stylesheet():
    return app.send_static_file("style.css")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")
