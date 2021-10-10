"""Stuff related to job control."""
import logging
import os
import subprocess

from werkzeug.utils import secure_filename

from mdpmflc.config import DPMDIR, DPMDRIVERS
from mdpmflc.errorhandlers import *
from mdpmflc.models import Job, db, Simulation

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


def queue_job(driver, series, label, configfile):
    """Queue a simulation."""
    # Check for duplication
    if Job.query.filter_by(series=series, label=label).all():
        raise SimulationAlreadyExistsError(
            driver, series, label,
            "That combination of series name and simulation label has already been used"
        )

    job = Job(
        driver=driver,
        series=series,
        label=label,
        config=configfile,
        status=0
    )
    db.session.add(job)
    db.session.commit()


def start_job(job_id: int) -> subprocess.Popen:
    job = Job.query.get_or_404(job_id)
    driver, series, label, config = job.driver, job.series, job.label, job.config

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
