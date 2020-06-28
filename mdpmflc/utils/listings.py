"""Utilities for producing listings of drivers, series, simulations, and
files of a simulation.
"""

import os
from mdpmflc import DPMDIR


def get_available_series():
    available_series = os.listdir(DPMDIR)
    available_series = [d for d in available_series if os.path.isdir(os.path.join(DPMDIR, d))]
    available_series = [d for d in available_series if d != "CMakeFiles"]
    available_series = sorted(available_series)
    return available_series


def get_available_simulations(sername):
    """List the simulations under the specified series. Returns None if
    there is no series of this name.
    """
    serdir = os.path.join(DPMDIR, sername)
    if os.path.isdir(serdir):
        available_simulations = [d for d in os.listdir(serdir) if (
                                    os.path.isdir(os.path.join(serdir, d))
                                    and os.path.isfile(os.path.join(serdir, d, f"{d}.config"))
                                )]
        print(available_simulations)
        available_simulations = sorted(available_simulations)
        return available_simulations
    else:
        return None
