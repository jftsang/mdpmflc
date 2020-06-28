#!/usr/bin/env python3
"""
Flask web interface for controlling MercuryDPM simulations and viewing
their results.

Please see README.md for full instructions. A quick guide in the
meantime:

Preparation:
    pip install Flask
    pip install matplotlib

To run:
    export FLASK_APP='mdpmflc.py'
    export FLASK_ENV='development'
    flask run --host=0.0.0.0 --debugger
"""
# Diagnosis
# import fnmatch
# from pprint import pprint, pformat

# Configuration
from . import app

# Utilities

# Controllers
import mdpmflc.controller.miscPages
import mdpmflc.controller.driver.viewDriver
import mdpmflc.controller.job.startJob
import mdpmflc.controller.results.simulation
import mdpmflc.controller.results.listing
import mdpmflc.controller.results.plots
import mdpmflc.controller.results.raw

# Error handlers
import mdpmflc.errorHandlers
