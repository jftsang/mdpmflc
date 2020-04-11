#!/usr/bin/env python3
"""
Flask web interface for controlling MercuryDPM simulations and viewing their results.

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
app = Flask(__name__)

# https://stackoverflow.com/a/50728936/12695048
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
# https://matplotlib.org/3.2.1/api/animation_api.html
from matplotlib.animation import FuncAnimation, ImageMagickWriter
# https://matplotlib.org/gallery/animation/dynamic_image2.html
import matplotlib.animation as animation

import random
from math import pi, sqrt
import numpy as np
import os
import fnmatch

from serve_raw_files import serve_data_raw, serve_fstat_raw, serve_restart_raw
from read_data_file import read_data_file


DPMDIR = "/media/asclepius/jmft2/MercuryDPM/MercuryBuild/Drivers/Tutorials"
DPMDRIVER = "/media/asclepius/jmft2/MercuryDPM/MercuryBuild/Drivers/Tutorials/Tutorial9"

def get_dt(sername, simname):
    """Get the timestep of a simulation (assuming that this doesn't
    change during a simulation).
    """
    data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.1")
    data_f = open(data_fn, "r")
    headline = data_f.readline().split(' ')
    return float(headline[1])


@app.route('/')
def mainpage():
    available_series = os.listdir(DPMDIR)
    available_series = [d for d in available_series if os.path.isdir(os.path.join(DPMDIR, d))]
    available_series = [d for d in available_series if d != "CMakeFiles"]
    available_series = sorted(available_series)
    return render_template("mainpage.html",
            hostname=flask.request.host,
            DPMDIR=DPMDIR,
            available_series=available_series)


@app.route('/results/')
def redirect_to_main(sername=None):
    return flask.redirect('/')


@app.route('/results/<sername>/')
def show_series(sername):
    serdir = os.path.join(DPMDIR, sername)
    if not os.path.isdir(serdir):
        # return f"The series {sername} does not exist."
        return flask.redirect(f"/results")

    available_simulations = [d for d in os.listdir(serdir) if os.path.isdir(os.path.join(serdir, d))]
    available_simulations = sorted(available_simulations)
    return render_template('show_series.html',
            hostname=flask.request.host,
            sername=sername,
            available_simulations=available_simulations)


@app.route('/results/<sername>/<simname>/')
def showsim(sername, simname):
    """Serve a page showing some summary statistics of this simulation,
    as well as links to more details such as individual files.
    """
    simdir = os.path.join(DPMDIR, sername, simname)
    if not os.path.isdir(simdir):
        # return f"The subdirectory {sername}/{simname} doesn't exist in the directory {DPMDIR}."
        return flask.redirect(f"/results/{sername}")

    files = os.listdir(simdir)
    files_parsed = [f.split(".") for f in files]
    max_data_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "data"])
    max_fstat_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "fstat"])
#    return render_template('simulation.html', sername=sername, simname=simname,
#            files=files_parsed, mdi=max_data_index, mfi=max_fstat_index)
    # FIXME at the moment it just goes to the 0th data file
    return flask.redirect(f"/results/{sername}/{simname}/0/data")



@app.route('/results/<sername>/<simname>/<ind>/')
@app.route('/results/<sername>/<simname>/<ind>/data/')
def showdatafile(sername, simname, ind):
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dimensions, headline, time, particles = read_data_file(dat_fn)

    if dimensions == 2:
        return render_template("data2d.html",
                sername=sername, simname=simname, ind=ind, time=time,
                dt=get_dt(sername, simname),
                headline=headline, lines=particles)

    if dimensions == 3:
        return render_template("data3d.html",
                sername=sername, simname=simname, ind=ind, time=time,
                dt=get_dt(sername, simname),
                headline=headline, lines=particles)


@app.route('/results/<sername>/<simname>/<ind>/fstat/')
def showfstatfile(sername, simname, ind):
    return ""


@app.route("/results/<sername>/<simname>/<ind>/plot/")
def showdataplot(sername, simname, ind):
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dimensions, headline, time, particles = read_data_file(dat_fn)

    if dimensions == 2:
        return render_template("data2d_plot.html",
                sername=sername, simname=simname, ind=ind, time=time,
                dt=get_dt(sername, simname),
                headline=headline, lines=particles)

    if dimensions == 3:
        return render_template("data3d_plot.html",
                sername=sername, simname=simname, ind=ind, time=time,
                dt=get_dt(sername, simname),
                headline=headline, lines=particles)


@app.route("/results/<sername>/<simname>/<ind>/plot/png")
def showdataplot_png(sername, simname, ind):
    data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")

    fig = create_figure(data_fn)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(data_fn):
    """Plots the data from a .data file."""
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)


    dimensions, headline, time, particles = read_data_file(data_fn)

    xs = [p[0] for p in particles]
    ys = [p[1] for p in particles]
    if dimensions == 2:
        rs = [p[5] for p in particles]
    if dimensions == 3:
        rs = [p[7] for p in particles]


    axis.scatter(xs, ys)
    # https://stackoverflow.com/questions/33094509/correct-sizing-of-markers-in-scatter-plot-to-a-radius-r-in-matplotlib#33095224
    # https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size#14860958
    # axis.scatter(xs, ys, s=[sqrt(r) for r in rs])

    if dimensions == 2:
        axis.set_xlim((headline[2], headline[4]))
        axis.set_ylim((headline[3], headline[5]))
    if dimensions == 3:
        axis.set_xlim((headline[2], headline[5]))
        axis.set_ylim((headline[3], headline[6]))
    axis.set_aspect('equal')

    axis.grid()
    return fig


@app.route('/style.css')
def stylesheet():
    return flask.url_for("static", filename="style.css")

