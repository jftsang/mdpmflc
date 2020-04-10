#!/bin/bash
source ./venv/bin/activate
export FLASK_APP='mdpmflc.py'
export FLASK_ENV='development'
flask run --host=0.0.0.0 --debugger >> flask.log 2>> flask.err &
