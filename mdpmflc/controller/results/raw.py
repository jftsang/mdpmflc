"""Endpoints that serve up raw output files."""
import os

from flask import Response

from mdpmflc import app
from mdpmflc.model.simulation import Simulation


@app.route('/results/<sername>/<simname>/data/<ind>/raw')
def serve_data_raw(sername, simname, ind):
    """Serve a raw .data. file."""
    sim = Simulation(sername, simname)
    dat_fn = sim.data_fn(ind)
    dat_f = open(dat_fn, "r")
    return Response(dat_f.read(), mimetype="text/plain")


@app.route('/results/<sername>/<simname>/fstat/<ind>/raw')
def serve_fstat_raw(sername, simname, ind):
    """Serve a raw .fstat. file."""
    sim = Simulation(sername, simname)
    fstat_fn = sim.fstat_fn(ind)
    fstat_f = open(fstat_fn, "r")
    return Response(fstat_f.read(), mimetype="text/plain")


@app.route('/results/<sername>/<simname>/restart/<ind>/raw')
def serve_restart_raw(sername, simname, ind):
    """Serve a raw .restart. file."""
    sim = Simulation(sername, simname)
    restart_fn = sim.restart_fn(ind)
    if not os.path.isfile(restart_fn):
        restart_fn = sim.restart_fn()

    restart_f = open(restart_fn, "r")
    return Response(restart_f.read(), mimetype="text/plain")
