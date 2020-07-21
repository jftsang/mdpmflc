"""Endpoints that serve up raw output files."""
import os

from flask import Response

from mdpmflc import DPMDIR
from mdpmflc import app


@app.route('/results/<sername>/<simname>/<ind>/data/raw')
def serve_data_raw(sername, simname, ind):
    """Serve a raw .data. file."""
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dat_f = open(dat_fn, "r")
    return Response(dat_f.read(), mimetype="text/plain")


@app.route('/results/<sername>/<simname>/<ind>/fstat/raw')
def serve_fstat_raw(sername, simname, ind):
    """Serve a raw .fstat. file."""
    fstat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.fstat.{ind}")
    fstat_f = open(fstat_fn, "r")
    return Response(fstat_f.read(), mimetype="text/plain")


@app.route('/results/<sername>/<simname>/<ind>/restart/raw')
def serve_restart_raw(sername, simname, ind):
    """Serve a raw .restart. file."""
    restart_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.restart.{ind}")
    if not os.path.isfile(restart_fn):
        restart_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.restart")

    restart_f = open(restart_fn, "r")
    return Response(restart_f.read(), mimetype="text/plain")
