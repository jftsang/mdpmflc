import os
import flask
from flask import Response, render_template

from mdpmflc import SRCDIR, app
from mdpmflc.utils.get_available_series import get_available_series


@app.route("/driver/<dri>/")
def driverpage(dri):
    """A page that shows information about a driver, with links to the
    driver's source, and a form for starting up a new simulation."""
    return render_template("driver.html",
                           hostname=flask.request.host,
                           driver=dri,
                           available_series=get_available_series())


@app.route("/driver/<dri>/source")
def driver_source(dri):
    """A page that shows a driver's source code."""
    src_fn = os.path.join(SRCDIR, dri + ".cpp")
    src_f = open(src_fn, "r")
    return render_template("driver_src.html",
                           driver=dri,
                           src=src_f.read())


@app.route("/driver/<dri>/source/raw")
def driver_source_raw(dri):
    """Return the driver's source code as a raw .cpp file."""
    src_fn = os.path.join(SRCDIR, dri + ".cpp")
    src_f = open(src_fn, "r")
    return Response(src_f.read(), mimetype='text/plain')
