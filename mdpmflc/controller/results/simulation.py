"""Pages that show processed results (not raw, no graphics) for a single
simulation.
"""
import os
import flask
from flask import render_template

from mdpmflc import DPMDIR, app
from mdpmflc.errorhandlers import SimulationNotFoundError
from mdpmflc.utils.simulation import get_simstatus, get_max_indices
from mdpmflc.utils.read_data_file import read_data_file
from mdpmflc.utils.read_restart_file import read_restart_file


@app.route('/results/<sername>/<simname>/')
def showsim(sername, simname):
    """Serve a page showing some summary statistics of this simulation,
    as well as links to more details such as individual files, and logs.
    """
    simdir = os.path.join(DPMDIR, sername, simname)
    if not os.path.isdir(simdir):
        # return f"The subdirectory {sername}/{simname} doesn't exist in the directory {DPMDIR}."
        raise SimulationNotFoundError(sername, simname)

    simstatus = get_simstatus(sername, simname)
    print(simstatus)

    max_data_index = simstatus['dataFileCounter']-1
    max_fstat_index = simstatus['fStatFileCounter']-1

    return render_template('simulation.html', sername=sername, simname=simname,
            simstatus=simstatus,
            dt=simstatus['timeStep'],
            mdi=max_data_index, mfi=max_fstat_index)


@app.route('/results/<sername>/<simname>/<ind>/data/')
def showdatafile(sername, simname, ind):
    simstatus = get_simstatus(sername, simname)
    max_data_index = simstatus['dataFileCounter']-1
    max_fstat_index = simstatus['fStatFileCounter']-1

    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dimensions, headline, time, particles = read_data_file(dat_fn)

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
    simstatus = get_simstatus(sername, simname)
    return ""


@app.route('/results/<sername>/<simname>/<ind>/')
@app.route("/results/<sername>/<simname>/<ind>/plot/")
def showdataplot(sername, simname, ind):
    """A page that contains a .data file's plot."""
    simstatus = get_simstatus(sername, simname)
    max_data_index = simstatus['dataFileCounter']-1
    max_fstat_index = simstatus['fStatFileCounter']-1

    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dimensions, headline, time, particles = read_data_file(dat_fn)

    if dimensions == 2:
        return render_template("results/data2d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep'],
                               headline=headline, lines=particles,
                               mdi=max_data_index)

    if dimensions == 3:
        return render_template("results/data3d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep'],
                               headline=headline, lines=particles,
                               mdi=max_data_index)
