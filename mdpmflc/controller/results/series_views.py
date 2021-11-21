"""Pages that show listings of series and simulations.
"""
import flask
from flask import render_template, Blueprint

from mdpmflc.utils.decorators import timed
from mdpmflc.utils.listings import get_available_simulations

series_views = Blueprint('series_views', __name__, )


@series_views.route("/<series>")
@timed("Showing series_view for {series}")
def series_view(series):
    """List the simulations belonging to a given series."""
    available_simulations = get_available_simulations(series)
    return render_template('show_series.html',
                           hostname=flask.request.host,
                           series=series,
                           available_simulations=available_simulations)
