"""Endpoints that serve up raw output files."""
import os

from flask import Response, Blueprint

from mdpmflc.models import Simulation

raw_file_views = Blueprint('raw_file_views', __name__, )

@raw_file_views.route('/<sername>/<simname>/data/<ind>/raw')
def serve_data_raw(sername, simname, ind):
    """Serve a raw .data. file."""
    sim = Simulation(sername, simname)
    dat_fn = sim.data_fn(ind)
    dat_f = open(dat_fn, "r")
    return Response(dat_f.read(), mimetype="text/plain")


@raw_file_views.route('/<sername>/<simname>/fstat/<ind>/raw')
def serve_fstat_raw(sername, simname, ind):
    """Serve a raw .fstat. file."""
    sim = Simulation(sername, simname)
    fstat_fn = sim.fstat_fn(ind)
    fstat_f = open(fstat_fn, "r")
    return Response(fstat_f.read(), mimetype="text/plain")


@raw_file_views.route('/<sername>/<simname>/ene/raw')
def serve_ene_raw(sername, simname):
    """Serve a raw .ene file."""
    sim = Simulation(sername, simname)
    ene_fn = sim.ene_fn()
    with open(ene_fn) as ene_f:
        return Response(ene_f.read(), mimetype="text/plain")


@raw_file_views.route('/<sername>/<simname>/restart/<ind>/raw')
def serve_restart_raw(sername, simname, ind):
    """Serve a raw .restart. file."""
    sim = Simulation(sername, simname)
    restart_fn = sim.restart_fn(ind)
    if not os.path.isfile(restart_fn):
        restart_fn = sim.restart_fn()

    restart_f = open(restart_fn, "r")
    return Response(restart_f.read(), mimetype="text/plain")
