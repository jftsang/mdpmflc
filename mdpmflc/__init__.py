"""Application-wide stuff for mdpmflc.
"""
from .config import DPMDIR, SRCDIR, CACHEDIR
import os

if not os.path.isdir(DPMDIR):
    raise FileNotFoundError(f"DPMDIR {DPMDIR} does not exist.")

if not os.path.isdir(SRCDIR):
    raise FileNotFoundError(f"SRCDIR {SRCDIR} does not exist.")

os.makedirs(CACHEDIR, mode=0o755, exist_ok=True)
