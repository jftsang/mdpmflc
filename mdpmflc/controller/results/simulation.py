"""Pages that show processed results (not raw, no graphics) for a single
simulation.
"""
import os
import flask
from flask import render_template

from mdpmflc import DPMDIR, app
from mdpmflc.utils.simulation import get_dt, get_max_indices
from mdpmflc.utils.read_data_file import read_data_file


@app.route('/results/<sername>/<simname>/')
def showsim(sername, simname):
    """Serve a page showing some summary statistics of this simulation,
    as well as links to more details such as individual files, and logs.
    """
    # FIXME at the moment it just goes to the 0th data file

    simdir = os.path.join(DPMDIR, sername, simname)
    if not os.path.isdir(simdir):
        # return f"The subdirectory {sername}/{simname} doesn't exist in the directory {DPMDIR}."
        return flask.redirect(f"/results/{sername}")

    files_parsed, max_data_index, max_fstat_index = get_max_indices(sername, simname)

    # FIXME serve up some useful information
#    return render_template('simulation.html', sername=sername, simname=simname,
#            files=files_parsed, mdi=max_data_index, mfi=max_fstat_index)

    return flask.redirect(f"/results/{sername}/{simname}/0/data")


@app.route('/results/<sername>/<simname>/<ind>/data/')
def showdatafile(sername, simname, ind):
    files_parsed, max_data_index, max_fstat_index = get_max_indices(sername, simname)
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dimensions, headline, time, particles = read_data_file(dat_fn)

    if dimensions == 2:
        return render_template("results/data2d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=get_dt(sername, simname),
                               headline=headline, lines=particles,
                               mdi=max_data_index)

    if dimensions == 3:
        return render_template("results/data3d.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=get_dt(sername, simname),
                               headline=headline, lines=particles,
                               mdi=max_data_index)


@app.route('/results/<sername>/<simname>/<ind>/fstat/')
def showfstatfile(sername, simname, ind):
    return ""
