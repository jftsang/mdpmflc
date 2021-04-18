import logging
import os
import subprocess

import flask
from flask import render_template

from mdpmflc import app
from mdpmflc.utils.jobs import queue_job


logging.getLogger().setLevel(logging.INFO)


@app.route("/queue", methods=["POST"])
def queue_a_simulation():
    """Receive a request for a simulation and queue it."""
    # https://code.luasoftware.com/tutorials/flask/flask-get-request-parameters-get-post-and-json/
    if flask.request.method == "GET":
        raise Exception("Sorry, you should request this page with a POST request")

    if "driver" in flask.request.values:
        driver = flask.request.values.get("driver")
    else:
        raise Exception("driver not given")

    if "sername" in flask.request.values:
        sername = flask.request.values.get("sername")
    else:
        raise Exception("sername not given")

    if "simname" in flask.request.values:
        simname = flask.request.values.get("simname")
        if not simname:  # empty string
            raise ValueError("simname should not be empty")
    else:
        raise Exception("simname not given")


    if "configfile" in flask.request.values:
        configfile = flask.request.values.get("configfile")
    else:
        raise Exception("Config file not given")

    logging.info(f"Received a job request for {driver}, {sername}/{simname}")

    subp = queue_job(driver, sername, simname, configfile)

    # return pformat(dir(flask.request.form))
    # return f"Started a run of driver {driver} on series {sername}, simulation name {simname}"
    # return Response(flask.request.get_json(), mimetype="application/json")
    return render_template("jobs/successful_queue.html",
                           hostname=flask.request.host,
                           driver=driver,
                           sername=sername,
                           simname=simname)
