"""Application-wide stuff for mdpmflc.
"""
import os
from flask import Flask
from .config import *

if not os.path.isdir(DPMDIR):
    raise FileNotFoundError(f"DPMDIR {DPMDIR} does not exist.")

if not os.path.isdir(SRCDIR):
    raise FileNotFoundError(f"SRCDIR {SRCDIR} does not exist.")

os.makedirs(CACHEDIR, mode=0o755, exist_ok=True)

app = Flask(__name__)
# db_engine = create_engine(f"sqlite:///{SQLITE_FILE}", echo=True)
