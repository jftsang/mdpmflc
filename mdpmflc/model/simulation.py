import os
from mdpmflc import DPMDIR
from mdpmflc.utils.read_file import read_restart_file


class Simulation:
    def __init__(self, sername, simname):
        self.sername = sername
        self.simname = simname

    def simdir(self):
        return os.path.join(DPMDIR, self.sername, self.simname)

    def data_fn(self, ind=None):
        """Return the path to a .data. file belonging to this
        simulation. If ind is not given then give the base name."""
        if ind:
            return os.path.join(self.simdir(), f"{self.simname}.data.{ind}")
        else:
            return os.path.join(self.simdir(), f"{self.simname}.data")

    def fstat_fn(self, ind=None):
        if ind:
            return os.path.join(self.simdir(), f"{self.simname}.fstat.{ind}")
        else:
            return os.path.join(self.simdir(), f"{self.simname}.fstat")

    def ene_fn(self):
        return os.path.join(self.simdir(), f"{self.simname}.ene")

    def restart_fn(self):
        return os.path.join(self.simdir(), f"{self.simname}.restart")

    def status(self):
        return read_restart_file(self.restart_fn(), header_only=True)

    def max_inds(self):
        """Give the maximum indices of .data. and .fstat. files that are
        present in the sim directory. This may be different from the
        indices recorded in the .restart file, if the counter has been
        reset.
        """
        files = os.listdir(self.simdir())
        files_parsed = [f.split(".") for f in files]
        max_data_index = max([int(fp[2]) for fp in files_parsed if len(fp) == 3 and fp[1] == "data"])
        max_fstat_index = max([int(fp[2]) for fp in files_parsed if len(fp) == 3 and fp[1] == "fstat"])
        return files_parsed, max_data_index, max_fstat_index
