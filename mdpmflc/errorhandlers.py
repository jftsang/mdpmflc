from flask import render_template

from mdpmflc.exceptions import SeriesNotFoundError, SimulationNotFoundError, SimulationAlreadyExistsError, \
    DriverNotFoundError


def driver_not_found_handler(error):
    return render_template('errors/drivernotfound.html', driver=str(error)), 500


def series_not_found_handler(error):
    return render_template('errors/seriesnotfound.html', sername=str(error)), 404


def simulation_not_found_handler(error):
    return render_template('errors/simulationnotfound.html',
                           sername=error.args[0],
                           simname=error.args[1]), 404


def simulation_already_exists_handler(error):
    return render_template('errors/simulationalreadyexists.html',
                           driver=error.args[0],
                           sername=error.args[1],
                           label=error.args[2],
                           message=str(error)), 409


def not_found_handler(error):
    """Catch-all 404 when a more appropriate error can't be given."""
    return render_template('errors/404.html'), 404


error_handlers = {
    DriverNotFoundError: driver_not_found_handler,
    SeriesNotFoundError: series_not_found_handler,
    SimulationNotFoundError: simulation_not_found_handler,
    SimulationAlreadyExistsError: simulation_already_exists_handler,
    404: not_found_handler,
}
