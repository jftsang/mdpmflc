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


@app.route('/style.css')
def stylesheet():
    return app.send_static_file("style.css")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")
