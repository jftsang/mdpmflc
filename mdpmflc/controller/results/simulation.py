"""Pages that show processed results (not raw, no graphics) for a single
simulation.
"""
import os
from flask import render_template

from mdpmflc import DPMDIR, app
from mdpmflc.errorhandlers import SimulationNotFoundError
from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.read_file import read_data_file


@app.route('/results/<sername>/<simname>/')
def showsim(sername, simname):
    """Serve a page showing some summary statistics of this simulation,
    as well as links to more details such as individual files, and logs.
    """
    sim = Simulation(sername, simname)
    if not os.path.isdir(sim.simdir()):
        # return f"The subdirectory {sername}/{simname} doesn't exist in the directory {DPMDIR}."
        raise SimulationNotFoundError(sername, simname)

    simstatus = sim.status()

    max_data_index = simstatus['dataFileCounter']-1
    max_fstat_index = simstatus['fStatFileCounter']-1

    return render_template('simulation.html', sername=sername, simname=simname,
                           simstatus=simstatus,
                           dt=simstatus['timeStep'],
                           mdi=max_data_index, mfi=max_fstat_index)


@app.route('/results/<sername>/<simname>/<ind>/data/')
def showdatafile(sername, simname, ind):
    sim = Simulation(sername, simname)
    simstatus = sim.status()
    max_data_index = simstatus['dataFileCounter']-1
    max_fstat_index = simstatus['fStatFileCounter']-1

    dimensions, headline, time, particles = read_data_file(sim.data_fn(ind))

    if dimensions == 2:
        return render_template("results/data2d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep'],
                               headline=headline, lines=particles,
                               mdi=max_data_index)

    if dimensions == 3:
        return render_template("results/data3d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep'],
                               headline=headline, lines=particles,
                               mdi=max_data_index)


@app.route('/results/<sername>/<simname>/<ind>/fstat/')
def showfstatfile(sername, simname, ind):
    return None


@app.route('/results/<sername>/<simname>/<ind>/')
@app.route("/results/<sername>/<simname>/<ind>/plot/")
def showdataplot(sername, simname, ind):
    """A page that contains a .data file's plot."""
    sim = Simulation(sername, simname)
    simstatus = sim.status()
    _, max_data_index, max_fstat_index = sim.max_inds()

    dimensions, headline, time, particles = read_data_file(sim.data_fn(ind))

    if dimensions == 2:
        return render_template("results/data2d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep'],
                               headline=headline, lines=particles,
                               mdi=max_data_index)

    elif dimensions == 3:
        return render_template("results/data3d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep'],
                               headline=headline, lines=particles,
                               mdi=max_data_index)

    else:
        raise ValueError("Number of dimensions should be 2 or 3.")
