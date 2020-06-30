import os
import subprocess

from mdpmflc import DPMDIR, DPMDRIVERS
from mdpmflc.errorhandlers import *
from mdpmflc.utils.listings import get_available_series

def start_job(driver, sername, simname):
    if driver not in DPMDRIVERS:
        raise Exception(f"{driver} is not a recognised driver.")

    if sername not in get_available_series():
        raise SeriesNotFoundError(sername)

    if not simname.isidentifier():
        raise ValueError(f"{simname} is an illegal name (fails isidentifier())")

    executable = os.path.join(DPMDIR, driver)
    simdir = os.path.join(DPMDIR, sername, simname)
    try:
        os.mkdir(simdir)
    except PermissionError as e:
        raise e  # TODO
    except FileExistsError as e:
        raise SimulationAlreadyExistsError(sername, simname, driver)

    # Start the simulation
    stdout_f = open(os.path.join(simdir, f"{simname}.log"), "a")
    stderr_f = open(os.path.join(simdir, f"{simname}.err"), "a")
    subprocess.run([executable, "-name", simname],
                   cwd=simdir,
                   stdout=stdout_f,
                   stderr=stderr_f)
