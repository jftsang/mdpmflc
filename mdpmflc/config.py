import os


MDPMFLCDIR = os.path.dirname(__file__)
# DPMDIR = "/Users/jmft2/s3gf"
DPMDIR = "/Volumes/Transcend/Fingering/"
SRCDIR = "/Volumes/Transcend/MercuryDPM/MercurySource/Drivers/USER/jmft2/Fingering"
CACHEDIR = "/tmp/mdpmflc.cache"
DPMDRIVERS = ["MaserFingering", "MdpmflcTutorial"]
CACHE_LIMIT = 500000000

SQLITE_FILE = os.path.join(MDPMFLCDIR, "./mdpmflc.db")
