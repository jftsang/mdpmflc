import flask
from flask import render_template

from mdpmflc.config import DPMDIR, DPMDRIVERS
from mdpmflc.utils.listings import get_available_series


def main_page():
    return render_template("mainpage.html",
                           hostname=flask.request.host,
                           DPMDIR=DPMDIR,
                           available_series=get_available_series(),
                           available_drivers=DPMDRIVERS)
