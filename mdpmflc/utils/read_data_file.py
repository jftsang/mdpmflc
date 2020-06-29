import random

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
