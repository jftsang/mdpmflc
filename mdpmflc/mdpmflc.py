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
from .utils.get_dt import get_dt
from .utils.get_available_series import get_available_series

# Controllers
from .controller.servePlots import *
from .controller.serveRawResults import *
from .controller.driver.viewDriver import *


@app.route('/')
def mainpage():
    return render_template("mainpage.html",
                           hostname=flask.request.host,
                           DPMDIR=DPMDIR,
                           available_series=get_available_series(),
                           available_drivers=DPMDRIVERS)


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


### Functions for serving up results


@app.route('/results/')
def redirect_to_main(sername=None):
    return flask.redirect('/')


@app.route('/results/<sername>/')
def show_series(sername):
    serdir = os.path.join(DPMDIR, sername)
    if not os.path.isdir(serdir):
        # return f"The series {sername} does not exist."
        return flask.redirect("/results")

    available_simulations = [d for d in os.listdir(serdir) if os.path.isdir(os.path.join(serdir, d))]
    available_simulations = sorted(available_simulations)
    return render_template('show_series.html',
                           hostname=flask.request.host,
                           sername=sername,
                           available_simulations=available_simulations)


def get_max_indices(sername, simname):
    simdir = os.path.join(DPMDIR, sername, simname)
    files = os.listdir(simdir)
    files_parsed = [f.split(".") for f in files]
    max_data_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "data"])
    max_fstat_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "fstat"])
    return files_parsed, max_data_index, max_fstat_index


@app.route('/results/<sername>/<simname>/')
def showsim(sername, simname):
    """Serve a page showing some summary statistics of this simulation,
    as well as links to more details such as individual files, and logs.
    """
    # FIXME at the moment it just goes to the 0th data file

    simdir = os.path.join(DPMDIR, sername, simname)
    if not os.path.isdir(simdir):
        # return f"The subdirectory {sername}/{simname} doesn't exist in the directory {DPMDIR}."
        return flask.redirect(f"/results/{sername}")

    files_parsed, max_data_index, max_fstat_index = get_max_indices(sername, simname)

    # FIXME serve up some useful information
#    return render_template('simulation.html', sername=sername, simname=simname,
#            files=files_parsed, mdi=max_data_index, mfi=max_fstat_index)

    return flask.redirect(f"/results/{sername}/{simname}/0/data")


@app.route('/results/<sername>/<simname>/<ind>/data/')
def showdatafile(sername, simname, ind):
    files_parsed, max_data_index, max_fstat_index = get_max_indices(sername, simname)
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dimensions, headline, time, particles = read_data_file(dat_fn)

    if dimensions == 2:
        return render_template("results/data2d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=get_dt(sername, simname),
                               headline=headline, lines=particles,
                               mdi=max_data_index)

    if dimensions == 3:
        return render_template("results/data3d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=get_dt(sername, simname),
                               headline=headline, lines=particles,
                               mdi=max_data_index)


@app.route('/results/<sername>/<simname>/<ind>/fstat/')
def showfstatfile(sername, simname, ind):
    return ""


### Miscellaneous

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


@app.route('/style.css')
def stylesheet():
    return app.send_static_file("style.css")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")
