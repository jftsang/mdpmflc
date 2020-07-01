import flask
from flask import render_template

from mdpmflc import app
from mdpmflc import DPMDIR, DPMDRIVERS
from mdpmflc.utils.listings import get_available_series


@app.route('/')
def mainpage():
    return render_template("mainpage.html",
                           hostname=flask.request.host,
                           DPMDIR=DPMDIR,
                           available_series=get_available_series(),
                           available_drivers=DPMDRIVERS)
