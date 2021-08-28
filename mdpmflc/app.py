#!/usr/bin/env python3
from flask import Flask

from .controller.driver.view_driver import driver_urls
from .controller.help import help_page
from .controller.job.start_job import queue_a_simulation
from .controller.miscPages import main_page
from .controller.results.listing import show_series, redirect_to_main
from .controller.results.plots import plots_urls
from .controller.results.plots_cg import cg_figure_view
from .controller.results.raw import raw_files_urls
from .controller.results.simulation import simulation_urls
from .errorhandlers import error_handlers

app = Flask(__name__)
app.add_url_rule("/", view_func=main_page)
app.add_url_rule("/help", view_func=help_page)

urls_dictionaries = [driver_urls, simulation_urls, raw_files_urls, plots_urls]

for urls in urls_dictionaries:
    for url in urls:
        app.add_url_rule(url, view_func=urls[url])

app.add_url_rule("/results/", view_func=redirect_to_main)
app.add_url_rule("/results/<sername>/", view_func=show_series)

app.add_url_rule("/plots/<sername>/<simname>/<ind>/<field>", view_func=cg_figure_view)

app.add_url_rule("/queue", view_func=queue_a_simulation, methods=["POST"])

for error in error_handlers:
    app.register_error_handler(error, error_handlers[error])

# db_engine = create_engine(f"sqlite:///{SQLITE_FILE}", echo=True)


def start_app():
    app.run(host="0.0.0.0", port="5000", debug=True)
