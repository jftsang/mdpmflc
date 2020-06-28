from mdpmflc import app
from flask import render_template


class SeriesNotFoundError(Exception):
    pass


class SimulationNotFoundError(Exception):
    pass


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(SeriesNotFoundError)
def series_not_found(error):
    return render_template('errors/seriesnotfound.html', sername=str(error)), 404


@app.errorhandler(SimulationNotFoundError)
def simulation_not_found(error):
    print(dir(error))
    return render_template('errors/simulationnotfound.html',
                           sername=error.args[0],
                           simname=error.args[1]), 404
