#!/usr/bin/env python3

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
import mdpmflc.errorhandlers

def start_app():
    app.run(host="0.0.0.0", port="5000", debug=True)
