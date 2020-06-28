import os
import subprocess

import flask
from flask import render_template

from mdpmflc import app, DPMDIR, DPMDRIVERS
from mdpmflc.utils.listings import get_available_series


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
        if sername not in get_available_series():
            raise ValueError(f"{sername} is not a recognised series.")
    else:
        raise Exception("sername not given")

    if "simname" in flask.request.values:
        simname = flask.request.values.get("simname")
        if not simname:  # empty string
            raise ValueError("simname should not be empty")
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
