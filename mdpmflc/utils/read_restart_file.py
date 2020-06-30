import linecache  # for reading large files
# https://stackoverflow.com/questions/2081836/reading-specific-lines-only


def read_restart_file(restart_fn, header_only=False):
    """Reads and parses a .restart file."""
    dic = dict()
    dic.update(read_restart_file_header(restart_fn))
    return dic


def read_restart_file_header(restart_fn):
    dic = dict()

    dataFile_line = linecache.getline(restart_fn, 2).strip().split()
    dic['dataFileCounter'] = int(dataFile_line[8])

    fStatFile_line = linecache.getline(restart_fn, 3).strip().split()
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
