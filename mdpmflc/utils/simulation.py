"""Tools for getting information about a simulation."""
import os
from mdpmflc import DPMDIR
from mdpmflc.utils.read_restart_file import read_restart_file

def get_simstatus(sername, simname):
    restart_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.restart")
    simstatus = read_restart_file(restart_fn, header_only=True)
    return simstatus


def get_dt(sername, simname):
    """Get the timestep of a simulation (assuming that this doesn't
    change during a simulation).
    """
    data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.1")
    data_f = open(data_fn, "r")
    headline = data_f.readline().split(' ')
    return float(headline[1])


def get_max_indices(sername, simname):
    simdir = os.path.join(DPMDIR, sername, simname)
    files = os.listdir(simdir)
    files_parsed = [f.split(".") for f in files]
    print(files_parsed)
    max_data_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "data"])
    max_fstat_index = max([int(fp[2]) for fp in files_parsed if fp[1] == "fstat"])
    return files_parsed, max_data_index, max_fstat_index
