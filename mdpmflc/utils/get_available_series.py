import os
from mdpmflc import DPMDIR


def get_available_series():
    available_series = os.listdir(DPMDIR)
    available_series = [d for d in available_series if os.path.isdir(os.path.join(DPMDIR, d))]
    available_series = [d for d in available_series if d != "CMakeFiles"]
    available_series = sorted(available_series)
    return available_series
