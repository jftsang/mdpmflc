import os
import subprocess
from werkzeug.utils import secure_filename

from mdpmflc.config import DPMDIR, DPMDRIVERS
from mdpmflc.errorhandlers import *
from mdpmflc.utils.listings import get_available_series

def start_job(driver, sername, simname, configfile):
    if driver not in DPMDRIVERS:
        raise Exception(f"{driver} is not a recognised driver.")

    if sername not in get_available_series():
        raise SeriesNotFoundError(sername)

    if not simname.isidentifier():
        raise ValueError(f"{simname} is an illegal name (fails isidentifier())")

    # Sanitise the uploaded config file and validate the filename
    filename = configfile.filename
    if not ('.' in filename and \
            filename.rsplit('.', 1)[1] == "config"):
        raise ValueError(f"{filename} is an illegal filename.")
    filename = secure_filename(filename)


    # Create a directory for the simulation
    simdir = os.path.join(DPMDIR, sername, simname)
    try:
        os.mkdir(simdir)
    except PermissionError as e:
        raise e  # TODO
    except FileExistsError as e:
        raise SimulationAlreadyExistsError(sername, simname, driver)

    # Put the uploaded config file there
    saveto = os.path.join(simdir, f"{simname}.config")
    if os.path.exists(saveto):
        raise SimulationAlreadyExistsError(sername, simname, driver)
    else:
        configfile.save(saveto)


    # Start the simulation
    executable = os.path.join(DPMDIR, driver)
    stdout_f = open(os.path.join(simdir, f"{simname}.log"), "a")
    stderr_f = open(os.path.join(simdir, f"{simname}.err"), "a")
    command = [executable, saveto, "-name", simname]
    print(command)

    subprocess.run([executable, f"{simname}.config", "-name", simname],
                   cwd=simdir,
                   stdout=stdout_f,
                   stderr=stderr_f)
