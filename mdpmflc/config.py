import os


MDPMFLCDIR = os.path.dirname(__file__)
DPMDIR = "/Users/jmft2/Fingering"
SRCDIR = "/Users/jmft2/MercuryDPM/MercurySource/Drivers/USER/jmft2/Fingering"

CACHEDIR = "/tmp/mdpmflc.cache"
DPMDRIVERS = ["MaserFingering", "MdpmflcTutorial"]
CACHE_LIMIT = 500000000

SQLITE_FILE = os.path.join(MDPMFLCDIR, "./mdpmflc.db")
