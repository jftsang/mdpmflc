#!/usr/bin/env python3

# Configuration
from mdpmflc import app

# Utilities

# Controllers
import mdpmflc.controller.driver.view_driver
import mdpmflc.controller.job.start_job
import mdpmflc.controller.results.simulation
import mdpmflc.controller.results.listing
import mdpmflc.controller.results.plots
import mdpmflc.controller.results.raw
import mdpmflc.controller.help
import mdpmflc.controller.miscPages

# Helpers
import mdpmflc.static
import mdpmflc.errorhandlers

def start_app():
    app.run(host="0.0.0.0", port="5000", debug=True)
