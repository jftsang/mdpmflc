#!/usr/bin/env python3
"""
Flask web interface for controlling MercuryDPM simulations and viewing
their results.

Please see README.md for full instructions. A quick guide in the
meantime:

Preparation:
    pip install -e .

To run:
    python -m mdpmflc
"""
import mdpmflc.app

mdpmflc.app.start_app()
