### Pages that serve up raw files
from flask import Flask, Response
import os
app = Flask(__name__)
DPMDIR = "/media/asclepius/jmft2/MercuryDPM/MercuryBuild/Drivers/Tutorials"

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
