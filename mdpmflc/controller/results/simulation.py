"""Pages that show processed results (not raw, no graphics) for a single
simulation.
"""
import os

from flask import render_template, Response

from mdpmflc.exceptions import SimulationNotFoundError
from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.read_file import (
    read_data_file,
)


def showsim(sername, simname):
    """Serve a page showing some summary statistics of this simulation,
    as well as links to more details such as individual files, and logs.
    """
    sim = Simulation(sername, simname)
    if not os.path.isdir(sim.simdir()):
        raise SimulationNotFoundError(sername, simname)

    simstatus = sim.status()
    print(simstatus)

    max_data_index = simstatus['dataFileCounter']-1
    print(max_data_index)
    max_fstat_index = simstatus['fStatFileCounter']-1

    return render_template('simulation.html', sername=sername, simname=simname,
                           simstatus=simstatus,
                           dt=simstatus['timeStep']*simstatus['dataFileSaveCount'],
                           mdi=max_data_index, mfi=max_fstat_index, ind=0)


def showconfig(sername, simname):
    sim = Simulation(sername, simname)
    with open(sim.config_fn(), "r") as config_f:
        return Response(config_f.read(), mimetype="text/plain")


def showlogout(sername, simname):
    sim = Simulation(sername, simname)
    with open(sim.out_fn(), "r") as out_f:
        return Response(out_f.read(), mimetype="text/plain")


def showlogerr(sername, simname):
    sim = Simulation(sername, simname)
    with open(sim.err_fn(), "r") as err_f:
        return Response(err_f.read(), mimetype="text/plain")


def showdatafile(sername, simname, ind):
    sim = Simulation(sername, simname)
    simstatus = sim.status()
    max_data_index = simstatus['dataFileCounter']-1
    max_fstat_index = simstatus['fStatFileCounter']-1

    ind = int(ind)
    if ind > max_data_index:
        return f"The index {ind} is greater than the maximum index {max_data_index} so far", 400

    try:
        data_df, dimensions, headline = read_data_file(sim.data_fn(ind))
    except FileNotFoundError:
        return f"{sim.data_fn(ind)} not found"
    num, time, xmin, ymin, zmin, xmax, ymax, zmax = headline

    if dimensions == 2:
        return render_template("results/data2d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep']*simstatus['dataFileSaveCount'],
                               lines=data_df,
                               mdi=max_data_index)

    if dimensions == 3:
        return render_template("results/data3d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep']*simstatus['dataFileSaveCount'],
                               lines=data_df,
                               mdi=max_data_index)


def showfstatfile(sername, simname, ind):
    raise NotImplementedError


def showdataplot_page(sername, simname, ind):
    """A page that contains a .data file's plot."""
    sim = Simulation(sername, simname)
    simstatus = sim.status()
    max_data_index = simstatus['dataFileCounter']-1

    data_df, dimensions, headline = read_data_file(sim.data_fn(ind))
    num, time, xmin, ymin, zmin, xmax, ymax, zmax = headline

    if dimensions == 2:
        return render_template("results/data2d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep']*simstatus['dataFileSaveCount'],
                               lines=data_df,
                               mdi=max_data_index)

    elif dimensions == 3:
        return render_template("results/data3d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=simstatus['timeStep']*simstatus['dataFileSaveCount'],
                               lines=data_df,
                               mdi=max_data_index)

    else:
        raise ValueError("Number of dimensions should be 2 or 3.")


simulation_urls = {
    "/results/<sername>/<simname>/": showsim,
    "/results/<sername>/<simname>/config": showconfig,
    "/results/<sername>/<simname>/config/raw": showconfig,
    "/results/<sername>/<simname>/log/": showlogout,
    "/results/<sername>/<simname>/log/out": showlogout,
    "/results/<sername>/<simname>/log/err": showlogerr,
    "/results/<sername>/<simname>/data/<ind>": showdatafile,
    "/results/<sername>/<simname>/fstat/<ind>": showfstatfile,
    "/results/<sername>/<simname>/plot/<ind>": showdataplot_page,
}
