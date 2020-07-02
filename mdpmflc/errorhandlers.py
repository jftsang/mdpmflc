from mdpmflc import app
from flask import Response, render_template


class DriverNotFoundError(Exception):
    pass


class SeriesNotFoundError(Exception):
    pass


class SimulationNotFoundError(Exception):
    pass


class SimulationAlreadyExistsError(Exception):
    pass


class IllegalSimulationNameError(Exception):
    pass


@app.errorhandler(DriverNotFoundError)
def driver_not_found(error):
    return render_template('errors/drivernotfound.html', driver=str(error)), 500


@app.errorhandler(SeriesNotFoundError)
def series_not_found(error):
    return render_template('errors/seriesnotfound.html', sername=str(error)), 404


@app.errorhandler(SimulationNotFoundError)
def simulation_not_found(error):
    return render_template('errors/simulationnotfound.html',
                           sername=error.args[0],
                           simname=error.args[1]), 404


@app.errorhandler(SimulationAlreadyExistsError)
def simulation_already_exists(error):
    return render_template('errors/simulationalreadyexists.html',
                           sername=error.args[0],
                           simname=error.args[1],
                           driver=error.args[2]), 409


@app.errorhandler(404)
def not_found(error):
    """Catch-all 404 when a more appropriate error can't be given."""
    return render_template('errors/404.html'), 404
