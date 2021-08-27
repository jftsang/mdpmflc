import os

import flask
from flask import Response, render_template

from mdpmflc import SRCDIR
from mdpmflc.utils.driver import get_config_fields
from mdpmflc.utils.listings import get_available_series


def driver_page(dri):
    """A page that shows information about a driver, with links to the
    driver's source, and a form for starting up a new simulation."""
    return render_template("driver.html",
                           hostname=flask.request.host,
                           driver=dri,
                           available_series=get_available_series())


def driver_source(dri):
    """A page that shows a driver's source code."""
    # Read the source file
    src_fn = os.path.join(SRCDIR, dri + ".cpp")
    src_f = open(src_fn, "r")
    src = src_f.read()

    # Read the example config, if it is available
    example_config_fn = os.path.join(SRCDIR, dri + ".example.config")
    try:
        example_config_f = open(example_config_fn, "r")
        example_config = example_config_f.read()
    except OSError:
        example_config = None

    pars_fields = get_config_fields(src, "pars")
    return render_template("driver_src.html",
                           driver=dri,
                           src=src,
                           cfgex=example_config,
                           pars_fields=pars_fields)


def driver_source_raw(dri):
    """Return the driver's source code as a raw .cpp file."""
    src_fn = os.path.join(SRCDIR, dri + ".cpp")
    src_f = open(src_fn, "r")
    return Response(src_f.read(), mimetype='text/plain')


def driver_source_exampleconfig(dri):
    """Return the example config file."""
    example_config_fn = os.path.join(SRCDIR, dri + ".example.config")
    try:
        example_config_f = open(example_config_fn, "r")
        example_config = example_config_f.read()
        return Response(example_config, mimetype='text/plain')
    except OSError:
        return Response(404)


driver_urls = {
    "/driver/<dri>/": driver_page,
    "/driver/<dri>/source": driver_source,
    "/driver/<dri>/source/raw": driver_source_raw,
    "/driver/<dri>/exampleconfig": driver_source_exampleconfig,
}
