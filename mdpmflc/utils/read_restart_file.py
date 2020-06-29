import linecache  # for reading large files
# https://stackoverflow.com/questions/2081836/reading-specific-lines-only


def read_restart_file(restart_fn, header_only=False):
    """Reads and parses a .restart file."""
    dic = dict()

    dataFile_line = linecache.getline(restart_fn, 2).strip().split()
    dic['dataFileCounter'] = int(dataFile_line[8])

    fStatFile_line = linecache.getline(restart_fn, 3).strip().split()
    dic['fStatFileCounter'] = int(fStatFile_line[8])

    time_line = linecache.getline(restart_fn, 9).strip().split()
    dic['timeStep'] = float(time_line[1])
    dic['time'] = float(time_line[3])
    dic['ntimeSteps'] = int(time_line[5])
    dic['timeMax'] = float(time_line[7])
    dic['ntimeStepsMax'] = int(dic['timeMax'] / dic['timeStep'])

    dic['progress'] = dic['time'] / dic['timeMax']

    return dic
