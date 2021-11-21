"""Utilities for producing listings of drivers, series, simulations, and
files of a simulation.
"""

import os
from typing import List

from mdpmflc import DPMDIR
from mdpmflc.exceptions import SeriesNotFoundError
from mdpmflc.models import Simulation


def get_available_series():
    available_series = os.listdir(DPMDIR)
    available_series = [
        d for d in available_series if os.path.isdir(os.path.join(DPMDIR, d))
    ]
    available_series = [d for d in available_series if d != "CMakeFiles"]
    available_series = sorted(available_series)
    return available_series


def get_available_simulations(series_name: str) -> List[Simulation]:
    """List the simulations under the specified series.
    """
    serdir = os.path.join(DPMDIR, series_name)
    if not os.path.isdir(serdir):
        raise SeriesNotFoundError

    simulation_names = [
        d
        for d in os.listdir(serdir)
        if (
            os.path.isdir(os.path.join(serdir, d))
            and os.path.isfile(os.path.join(serdir, d, f"{d}.config"))
        )
    ]
    simulations = [
        Simulation(series_name, label) for label in sorted(simulation_names)
    ]
    return simulations
