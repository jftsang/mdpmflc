from collections import namedtuple
import os
import random
import linecache  # for reading large files
import pandas as pd
# https://stackoverflow.com/questions/2081836/reading-specific-lines-only


def read_ene_file(ene_fn):
    """Read the information from an .ene file."""
    return pd.read_csv(ene_fn, sep='\s+')


def read_restart_file(restart_fn, header_only=False):
    """Reads and parses a .restart file. Raises FileNotFoundError if
    the file doesn't exist
    """
    if not os.path.isfile(restart_fn):
        raise FileNotFoundError(f"{restart_fn} does not exist.")
    dic = dict()
    dic.update(read_restart_file_header(restart_fn))
    return dic


def read_restart_file_header(restart_fn):
    dic = dict()

    dataFile_line = linecache.getline(restart_fn, 2).strip().split()
    dic['dataFileSaveCount'] = int(dataFile_line[6])
    dic['dataFileCounter'] = int(dataFile_line[8])

    fStatFile_line = linecache.getline(restart_fn, 3).strip().split()
    dic['fStatFileSaveCount'] = int(fStatFile_line[6])
    dic['fStatFileCounter'] = int(fStatFile_line[8])

    domain_line = linecache.getline(restart_fn, 8).strip().split()
    dic['xMin'] = float(domain_line[1])
    dic['xMax'] = float(domain_line[3])
    dic['yMin'] = float(domain_line[5])
    dic['yMax'] = float(domain_line[7])
    dic['zMin'] = float(domain_line[9])
    dic['zMax'] = float(domain_line[11])

    time_line = linecache.getline(restart_fn, 9).strip().split()
    dic['timeStep'] = float(time_line[1])
    dic['time'] = float(time_line[3])
    dic['ntimeSteps'] = int(time_line[5])
    dic['timeMax'] = float(time_line[7])
    dic['ntimeStepsMax'] = int(dic['timeMax'] / dic['timeStep'])

    dic['progress'] = dic['time'] / dic['timeMax']

    misc_line = linecache.getline(restart_fn, 10).strip().split()
    dic['gx'] = float(misc_line[5])
    dic['gy'] = float(misc_line[6])
    dic['gz'] = float(misc_line[7])

    return dic

DataFile = namedtuple(
    'DataFile',
    ['header', 'data_df']
)

DataFileHeadline = namedtuple(
    'DataFileHeadline',
    ['num', 'time', 'xmin', 'ymin', 'zmin', 'xmax', 'ymax', 'zmax']
)


def read_data_file_headline(filename):
    with open(filename) as data_f:
        headline = data_f.readline().strip().split(' ')

    if len(headline) == 6:
        dimensions = 2
        headline = DataFileHeadline(
            num=int(headline[0]),
            time=float(headline[1]),
            xmin=float(headline[2]),
            ymin=float(headline[3]),
            zmin=0,
            xmax=float(headline[4]),
            ymax=float(headline[5]),
            zmax=0
        )

    elif len(headline) == 8:
        dimensions = 3
        headline = DataFileHeadline(
            num=int(headline[0]),
            time=float(headline[1]),
            xmin=float(headline[2]),
            ymin=float(headline[3]),
            zmin=float(headline[4]),
            xmax=float(headline[5]),
            ymax=float(headline[6]),
            zmax=float(headline[7])
        )

    else:
        raise ValueError

    # Determine the dimensionality of the simulation from the length of the first line

    return dimensions, *headline


def read_data_file(filename):
    dimensions, num, time, xmin, ymin, zmin, xmax, ymax, zmax = read_data_file_headline(filename)
    if dimensions == 2:
        column_names = ['x', 'y', 'u', 'v', 'r', 'th', 'om', 'sp']
    if dimensions == 3:
        column_names = [
            'x', 'y', 'z', 'u', 'v', 'w', 'r',
            'alpha', 'beta', 'gamma', 'omex', 'omey', 'omez', 'sp'
        ]

    data_df = pd.read_csv(
        filename,
        skiprows=1,
        header=None,
        sep=' ',
        names=column_names
    )
    return data_df, dimensions, num, time, xmin, ymin, zmin, xmax, ymax, zmax
