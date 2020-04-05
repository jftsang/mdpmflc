"""
Flask web interface for controlling MercuryDPM simulations and viewing their results.

Preparation:
    pip install Flask

To run:
    export FLASK_APP='mdpmflc.py'
    export FLASK_ENV='development'
    flask run --host=0.0.0.0 --debugger
"""

import flask
from flask import Flask, Response
from flask import render_template
app = Flask(__name__)

import os
import fnmatch

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
    dat_f = open(dat_fn, "r")

    headline = dat_f.readline().strip().split(' ')
    if len(headline) == 6:
        dimensions = 2
    elif len(headline) == 8:
        dimensions = 3
    else:
        raise ValueError

    np = int(headline[0])
    time = float(headline[1])

    if np <= 50:
        lines = dat_f.readlines() # FIXME don't read in all lines (dangerous for big files)
    else:
        lines = []
        for i in range(50):
            lines.append(dat_f.readline().strip())


    if dimensions == 2:
        return render_template("data2d.html",
                sername=sername, simname=simname, ind=ind, time=time,
                dt=get_dt(sername, simname),
                headline=headline, lines=lines)

    if dimensions == 3:
        return render_template("data3d.html",
                sername=sername, simname=simname, ind=ind, time=time,
                dt=get_dt(sername, simname),
                headline=headline, lines=lines)


### Pages that serve up raw files

@app.route('/results/<sername>/<simname>/<ind>/data/raw')
def erve_data_raw(sername, simname, ind):
    """Serve a raw .data. file."""
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dat_f = open(dat_fn, "r")
    return Response(dat_f.read(), mimetype="text/plain")


@app.route('/results/<sername>/<simname>/<ind>/fstat/raw')
def erve_fstat_raw(sername, simname, ind):
    """Serve a raw .fstat. file."""
    fstat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.fstat.{ind}")
    fstat_f = open(fstat_fn, "r")
    return Response(fstat_f.read(), mimetype="text/plain")


@app.route('/results/<sername>/<simname>/<ind>/restart/raw')
def serve_restart_raw(sername, simname, ind):
    """Serve a raw .restart. file."""
    restart_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.restart.{ind}")
    restart_f = open(restart_fn, "r")
    return Response(restart_f.read(), mimetype="text/plain")


@app.route('/style.css')
def stylesheet():
    return flask.url_for("static", filename="style.css")
