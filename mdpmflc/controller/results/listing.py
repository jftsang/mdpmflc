"""Pages that show listings of series and simulations.
"""
import flask
from flask import render_template

from mdpmflc import DPMDIR, app
from mdpmflc.errorHandlers import SeriesNotFoundError
from mdpmflc.utils.listings import get_available_simulations


@app.route('/results/')
def redirect_to_main(sername=None):
    return flask.redirect('/')


@app.route('/results/<sername>/')
def show_series(sername):
    available_simulations = get_available_simulations(sername)
    if available_simulations is None:
        raise SeriesNotFoundError(sername)

    return render_template('show_series.html',
                           hostname=flask.request.host,
                           sername=sername,
                           available_simulations=available_simulations)
