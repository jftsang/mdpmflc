import os

from flask import render_template
from mdpmflc import SRCDIR


def help_page():
    """A page that shows help."""
    # src_fn = os.path.join(SRCDIR, "MdpmflcTutorial" + ".cpp")
    src_fn = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)), "..", "static", "MdpmflcTutorial.cpp")
    src_f = open(src_fn, "r")
    example_driver_src = src_f.read()

    ex_fn = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)), "..", "static", "mdpmflc_example.config")
    ex_f = open(ex_fn, "r")
    example_config = ex_f.read()

    return render_template("help.html",
                           example_driver_src=example_driver_src,
                           example_config=example_config)
