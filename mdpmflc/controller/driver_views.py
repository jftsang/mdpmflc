import os

import flask
from flask import Response, render_template, Blueprint
from flask_breadcrumbs import register_breadcrumb

from mdpmflc import SRCDIR
from mdpmflc.models import Driver
from mdpmflc.utils.driver import get_config_fields
from mdpmflc.utils.listings import get_available_series

driver_views = Blueprint('driver_views', __name__, )


@driver_views.route("/<driver>")
@register_breadcrumb(driver_views, '.<driver>', 'Driver')
def driver_page(driver):
    """A page that shows information about a driver, with links to the
    driver's source, and a form for starting up a new simulation."""
    return render_template("drivers/driver.html",
                           hostname=flask.request.host,
                           driver=driver,
                           available_series=get_available_series())


@driver_views.route("/<driver_name>/source")
@register_breadcrumb(driver_views, '.<driver_name>.source', 'Driver source')
def driver_source(driver_name):
    """A page that shows a driver's source code."""
    # Read the source file
    driver = Driver.query.filter_by(name=driver_name).one()
    try:
        with open(driver.src_path) as src_f:
            src = src_f.read()
            pars_fields = get_config_fields(src, "pars")
    except (TypeError, FileNotFoundError):
        src = ""
        pars_fields = []

    # Read the example config, if it is available
    try:
        with open(driver.example_path) as example_config_f:
            example_config = example_config_f.read()
    except (TypeError, FileNotFoundError):
        example_config = None

    return render_template("drivers/driver_src.html",
                           driver=driver_name,
                           src=src,
                           cfgex=example_config,
                           pars_fields=pars_fields)


@driver_views.route("/<driver_name>/source/raw")
def driver_source_raw(driver_name):
    """Return the driver's source code as a raw .cpp file."""
    driver = Driver.query.filter_by(name=driver_name).one()
    with open(driver.src_path) as src_f:
        return Response(src_f.read(), mimetype='text/plain')


@driver_views.route("/<driver_name>/exampleconfig")
def driver_source_exampleconfig(driver_name):
    """Return the example config file."""
    driver = Driver.query.filter_by(name=driver_name).one()
    with open(driver.example_path) as example_f:
        return Response(example_f.read(), mimetype='text/plain')
