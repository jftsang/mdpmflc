import os
from datetime import datetime, timedelta
from functools import wraps
from os.path import getctime
from typing import Tuple, Any

import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableDict

from mdpmflc import DPMDIR
from mdpmflc.utils.decorators import Maybe
from mdpmflc.utils.read_file import read_restart_file

db = SQLAlchemy()


class Driver(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100))
    src_path = db.Column(db.String(500))
    example_path = db.Column(db.String(500))
    bin_path = db.Column(db.String(500))

    def __str__(self):
        return self.name

    __repr__ = __str__


class Series(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100))

    def __str__(self):
        return self.name

    __repr__ = __str__


class Job(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    driver = db.relationship("Driver", backref=db.backref("driver", uselist=False))

    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    series = db.relationship("Series", backref=db.backref("series", uselist=False))

    label = db.Column(db.String(100), nullable=False)
    config = db.Column(db.Text())
    submitted_date = db.Column(db.DateTime(), default=datetime.utcnow)
    command = db.Column(db.String(500))
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, driver, series, label, config, status):
        self.driver = driver
        self.series = series
        self.label = label
        self.config = config
        self.status = status

    def __str__(self):
        return f"{self.series}: {self.label}, running {self.driver}"

    __repr__ = __str__


class Simulation:
    def __init__(self, sername, label):
        self.sername = sername
        self.label = label

    def __str__(self):
        return self.label

    __repr__ = __str__

    def simdir(self):
        return os.path.join(DPMDIR, self.sername, self.label)

    def config_fn(self):
        return os.path.join(self.simdir(), f"{self.label}.config")

    def out_fn(self):
        # return os.path.join(self.simdir(), f"{self.simname}.log")
        return os.path.join(self.simdir(), "cout")

    def err_fn(self):
        # return os.path.join(self.simdir(), f"{self.simname}.err")
        return os.path.join(self.simdir(), "cerr")

    def data_fn(self, ind=None):
        """Return the path to a .data. file belonging to this
        simulation. If ind is not given then give the base name.
        """
        if ind is not None:
            return os.path.join(self.simdir(), f"{self.label}.data.{ind}")
        else:
            return os.path.join(self.simdir(), f"{self.label}.data")

    def fstat_fn(self, ind=None):
        if ind is not None:
            return os.path.join(self.simdir(), f"{self.label}.fstat.{ind}")
        else:
            return os.path.join(self.simdir(), f"{self.label}.fstat")

    def ene_fn(self):
        return os.path.join(self.simdir(), f"{self.label}.ene")

    def restart_fn(self, ind=None) -> str:
        if ind is not None:
            return os.path.join(self.simdir(), f"{self.label}.restart.{ind}")
        else:
            return os.path.join(self.simdir(), f"{self.label}.restart")

    def status(self) -> ImmutableDict:
        return read_restart_file(self.restart_fn(), header_only=True)

    def max_indices(self) -> Tuple[Any, int, int]:
        """Give the maximum indices of .data. and .fstat. files that are
        present in the sim directory. This may be different from the
        indices recorded in the .restart file, if the counter has been
        reset.
        """
        files = os.listdir(self.simdir())
        files_parsed = [f.split(".") for f in files]

        maybe_max = Maybe(ValueError)(max)
        max_data_index = maybe_max([int(file[2]) for file in files_parsed if len(file) == 3 and file[1] == "data"])
        max_fstat_index = maybe_max([int(file[2]) for file in files_parsed if len(file) == 3 and file[1] == "fstat"])
        return files_parsed, max_data_index, max_fstat_index

    def file_list(self):
        """List of files belonging to the simulation, in the simdir."""
        return os.listdir(self.simdir())

    @Maybe(ValueError, FileNotFoundError)
    def time_to_complete(self) -> timedelta:
        file_0 = self.data_fn(0)
        _, max_data_index, _ = self.max_inds()
        file_recent = self.data_fn(max_data_index)
        diff_time = getctime(file_recent) - getctime(file_0)
        return timedelta(seconds=diff_time)


class DataFile:
    """A class that represents a .data file."""

    def __init__(self, sim: Simulation, ind: int):
        self.sim = sim
        self.ind = ind
        self.dimensions = None
        self.headline = None
        self.df = None

    def read_header(self):
        """Read the first line of the .data file."""
        data_fn = self.sim.data_fn(self.ind)
        with open(data_fn, "r") as data_f:
            headline = data_f.readline().strip().split(' ')

        # Convert these to numeric values. The first number is the
        # number of particles, and needs to be an int. The rest are
        # floats.
        headline = (int(headline[0]), *[float(h) for h in headline[1:]])

        # Determine the dimensionality of the simulation from the length
        # of the first line. Also the column headers.
        if len(headline) == 6:
            self.dimensions = 2
        elif len(headline) == 8:
            self.dimensions = 3
        else:
            raise ValueError

        # number of particles
        self.np = int(headline[0])
        # time
        self.time = float(headline[1])

        self.headline = headline

    def read(self):
        """Read the contents of the .data file. Return the particles'
        information as a pandas dataframe.
        """
        if not self.headline:
            self.read_header()
        if self.df is not None:
            return self.df

        data_fn = self.sim.data_fn(self.ind)
        if self.dimensions == 2:
            names = ['x', 'y', 'u', 'v', 'r', 'theta', 'omega', 'species']
        elif self.dimensions == 3:
            names = ['x', 'y', 'z', 'u', 'v', 'w', 'r', 'th1', 'th2', 'th3', 'o1', 'om2', 'om3', 'species']
        else:
            raise ValueError
        self.df = pd.read_csv(data_fn, sep=" ", skiprows=1, names=names)
        return self.df
