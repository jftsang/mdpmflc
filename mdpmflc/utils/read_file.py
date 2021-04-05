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


def read_data_file(data_fn, samplesize=None):
    """Reads and parses a .data file. Returns a tuple (dimensions, headline, particles)
    where dimensions is an integer that is either 2 or 3,
          headline is a list
          particles is a list of lists
    """
    data_f = open(data_fn, "r")

    headline = data_f.readline().strip().split(' ')
    headline = [int(headline[0])] + [float(h) for h in headline[1:]] # FIXME bit of a kludge

    # Determine the dimensionality of the simulation from the length of the first line
    if len(headline) == 6:
        dimensions = 2
    elif len(headline) == 8:
        dimensions = 3
    else:
        raise ValueError

    # time
    time = float(headline[1])

    # number of particles
    np = int(headline[0])
    # don't read in all lines (dangerous for big files)
    particles = []

    chance = samplesize/np if samplesize is not None else 1
    random.seed()

    for line in data_f:
        cells = line.strip().split(' ')
        if random.random() < chance:
            particles.append([float(c) for c in cells])

#        if len(particles) >= samplesize:
#            break

    return dimensions, headline, time, particles


def read_data_file_particle(data_fn, pid=0):
    """Reads and parses a .data file, getting the (pid)th particle.
    Returns a tuple (dimensions, headline, times, points)
    where dimensions is an integer that is either 2 or 3,
          headline is a list
          particles is a list of lists
    """
    data_f = open(data_fn, "r")

    headline = data_f.readline().strip().split(' ')
    headline = [int(headline[0])] + [float(h) for h in headline[1:]] # FIXME bit of a kludge
    print(headline)

    # Determine the dimensionality of the simulation from the length of the first line
    if len(headline) == 6:
        dimensions = 2
    elif len(headline) == 8:
        dimensions = 3
    else:
        raise ValueError

    # time
    time = float(headline[1])

    # number of particles
    np = int(headline[0])
    # don't read in all lines (dangerous for big files)
    particles = []
    for i in range(min(np, maxlines)): # TODO is this the best way? First n might not be a good sample.
        cells = data_f.readline().split(' ')
        particles.append([float(c) for c in cells])

    return dimensions, headline, time, particles
