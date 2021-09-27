"""Stuff related to job control."""
import logging
import os
import sqlite3
import subprocess

import pandas as pd
from werkzeug.utils import secure_filename

from mdpmflc.config import DPMDIR, DPMDRIVERS, SQLITE_FILE
from mdpmflc.errorhandlers import *
from mdpmflc.model.job import Job, db
from mdpmflc.model.simulation import Simulation
from mdpmflc.utils.listings import get_available_series

logging.getLogger().setLevel(logging.INFO)

def sanitise_filename(filename):
    """Sanitise the uploaded config file's filename. Raise an exception
    if the filename doesn't have a proper extension.

    @param configfile An uploaded file, from flask.request.files.get("configfile").
    """
    print(filename)
    print(filename.rsplit('.', 1))
    if not ('.' in filename and \
            filename.rsplit('.',  1)[1] in ["txt", "config"]):
        raise ValueError(f"{filename} is an illegal filename. It should have .txt or .config extension.)")
    filename = secure_filename(filename)

    return filename


def queue_job(driver, sername, simname, configfile):
    """Queue a simulation."""

    if driver not in DPMDRIVERS:
        raise Exception(f"{driver} is not a recognised driver.")

    if sername not in get_available_series():
        raise SeriesNotFoundError(sername)

    if not simname.isidentifier():
        raise ValueError(f"{simname} is an illegal name (fails isidentifier())")

    # Check for duplication
    queue = get_queue()
    if any((queue.series == sername) & (queue.simname == simname)):
        raise SimulationAlreadyExistsError(
            driver, sername, simname,
            "That combination of series and simulation name has already been used"
        )

    with sqlite3.connect(SQLITE_FILE) as conn:
        pd.DataFrame({
            'simname': [simname],
            'series': [sername],
            'driver': [driver],
            'config': [configfile],
            'status': [0]
        }).to_sql('jobs', conn, if_exists='append', index=False)


def get_queue():
    with sqlite3.connect(SQLITE_FILE) as conn:
        return pd.read_sql_query("SELECT * FROM jobs", conn)


def start_job(job_id):
    job = Job.query.filter_by(job_id=job_id)
    driver, series, label, config = job.driver, job.series, job.simulation, job.config

    # Create a directory for the simulation
    sim = Simulation(series, label)
    simdir = sim.simdir()
    try:
        os.mkdir(simdir)
    except PermissionError as e:
        raise e  # TODO
    except FileExistsError as e:
        raise SimulationAlreadyExistsError(series, label, driver)

    # Put the uploaded config file there
    saveto = sim.config_fn()
    if os.path.exists(saveto):
        raise SimulationAlreadyExistsError(series, label, driver)

    with open(saveto, "w") as fp:
        fp.write(config)
        logging.info(f"Saved config file to {saveto}")

    # Queue the simulation
    executable = os.path.join(DPMDIR, driver)
    stdout_f = open(sim.out_fn(), "a")
    stderr_f = open(sim.err_fn(), "a")
    command = [executable, saveto, "-name", label]

    print(command)
    subp = subprocess.Popen(['echo'] + command,
                            cwd=simdir,
                            stdout=stdout_f,
                            stderr=stderr_f)

    job.status = 1
    db.session.commit()


    return subp


def does_simulation_already_exist(sername, simname):
    raise NotImplementedError
