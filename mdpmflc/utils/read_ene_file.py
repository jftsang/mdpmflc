def read_ene_file(ene_fn):
    """Read the information from an .ene file."""
    ts = []
    gpes = []
    kes = []
    with open(ene_fn, "r") as ene_f:
        ene_f.readline()  # discard the first line
        for x in ene_f:
            line = x.strip().split()
            line = [float(l) for l in line]
            ts.append(line[0])
            gpes.append(line[1])
            kes.append(line[2])

    return ts, gpes, kes
