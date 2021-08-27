"""Endpoints that serve up raw output files."""
import os

from flask import Response

from mdpmflc.model.simulation import Simulation


def serve_data_raw(sername, simname, ind):
    """Serve a raw .data. file."""
    sim = Simulation(sername, simname)
    dat_fn = sim.data_fn(ind)
    dat_f = open(dat_fn, "r")
    return Response(dat_f.read(), mimetype="text/plain")


def serve_fstat_raw(sername, simname, ind):
    """Serve a raw .fstat. file."""
    sim = Simulation(sername, simname)
    fstat_fn = sim.fstat_fn(ind)
    fstat_f = open(fstat_fn, "r")
    return Response(fstat_f.read(), mimetype="text/plain")


def serve_ene_raw(sername, simname):
    """Serve a raw .ene file."""
    sim = Simulation(sername, simname)
    ene_fn = sim.ene_fn()
    with open(ene_fn) as ene_f:
        return Response(ene_f.read(), mimetype="text/plain")


def serve_restart_raw(sername, simname, ind):
    """Serve a raw .restart. file."""
    sim = Simulation(sername, simname)
    restart_fn = sim.restart_fn(ind)
    if not os.path.isfile(restart_fn):
        restart_fn = sim.restart_fn()

    restart_f = open(restart_fn, "r")
    return Response(restart_f.read(), mimetype="text/plain")


raw_files_urls = {
    "/results/<sername>/<simname>/data/<ind>/raw": serve_data_raw,
    "/results/<sername>/<simname>/fstat/<ind>/raw": serve_fstat_raw,
    "/results/<sername>/<simname>/ene/raw": serve_ene_raw,
    "/results/<sername>/<simname>/restart/<ind>/raw": serve_restart_raw,
}
