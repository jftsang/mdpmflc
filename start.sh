#!/bin/bash
set -eux
source ./venv/bin/activate
sqlite3 -echo mdpmflc/mdpmflc.db < database.sql
python -m mdpmflc
