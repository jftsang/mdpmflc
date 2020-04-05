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

#@app.route('/hello/')
#@app.route('/hello/<name>')
#def hello(name=None):
#    return render_template('hello.html', name=name)

@app.route('/')
def mainpage():
    available_series = os.listdir(DPMDIR)
    available_series = [d for d in available_series if os.path.isdir(os.path.join(DPMDIR, d))]
    return render_template("mainpage.html",
            hostname=flask.request.host,
            DPMDIR=DPMDIR,
            available_series=available_series)

@app.route('/filelist')
@app.route('/filelist/<sername>')
def redirect_to_main(sername=None):
    return flask.redirect('/')

@app.route('/filelist/<sername>/<simname>')
def filelist_for_sim(sername, simname):
    simdir = os.path.join(DPMDIR, sername, simname)
    if os.path.isdir(simdir):
        files = os.listdir(simdir)
        files_parsed = [f.split(".") for f in files]
        max_data_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "data"])
        max_fstat_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "fstat"])
        return render_template('filelist.html', sername=sername, simname=simname,
                files=files_parsed, mdi=max_data_index, mfi=max_fstat_index)
    else:
        return f"The subdirectory {sername} doesn't exist in the directory {DPMDIR}"

@app.route('/data/<sername>/<simname>/<ind>/')
def showdatafile(sername, simname, ind):
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dat_f = open(dat_fn, "r")

    headline = dat_f.readline().split(' ')
    dimensions = int(headline[0])
    time = headline[1]

    lines = dat_f.readlines()
    if dimensions == 3:
        return render_template("datafile.html",
                sername=sername, simname=simname, ind=ind, time=time,
                headline=headline, lines=lines)

@app.route('/data/<sername>/<simname>/<ind>/raw')
def showdatafile_raw(sername, simname, ind):
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dat_f = open(dat_fn, "r")
    return Response(dat_f.read(), mimetype="text/plain")
