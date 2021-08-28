"""Pages that show listings of series and simulations.
"""
import flask
from flask import render_template, Blueprint

from mdpmflc.exceptions import SeriesNotFoundError
from mdpmflc.utils.listings import get_available_simulations

series_views = Blueprint('series_views', __name__, )


@series_views.route("/<sername>")
def series_view(sername):
    """List the simulations belonging to a given series."""
    available_simulations = get_available_simulations(sername)
    if available_simulations is None:
        raise SeriesNotFoundError(sername)

    return render_template('show_series.html',
                           hostname=flask.request.host,
                           sername=sername,
                           available_simulations=available_simulations)
