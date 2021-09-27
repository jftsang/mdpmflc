#!/usr/bin/env python3
from flask import Flask

from mdpmflc.controller.driver_views import driver_views
from mdpmflc.controller.job_views import job_views
from .config import SQLITE_FILE
from .controller.results.cg_plots_figviews import cg_plots_figviews
from .controller.results.plots_figviews import plots_figviews
from .controller.results.raw_file_views import raw_file_views
from .controller.results.series_views import series_views
from .controller.results.simulation_views import simulation_views
from .controller.static_views import static_views
from .errorhandlers import error_handlers


def create_app():
    app = Flask(__name__)

    app.register_blueprint(static_views, url_prefix="/")
    app.register_blueprint(driver_views, url_prefix="/driver")
    app.register_blueprint(series_views, url_prefix="/results")
    app.register_blueprint(simulation_views, url_prefix="/results")
    app.register_blueprint(raw_file_views, url_prefix="/results")
    app.register_blueprint(plots_figviews, url_prefix="/plots")
    app.register_blueprint(cg_plots_figviews, url_prefix="/plots")
    app.register_blueprint(job_views, url_prefix="/jobs")

    for error in error_handlers:
        app.register_error_handler(error, error_handlers[error])


    # Be permissive about trailing slashes https://stackoverflow.com/a/40365514
    app.url_map.strict_slashes = False

    @app.before_request
    def clear_trailing_slashes():
        from flask import redirect, request

        rp = request.path
        if rp != '/' and rp.endswith('/'):
            return redirect(rp[:-1])

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{SQLITE_FILE}'

    return app


def start_app():
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

# db_engine = create_engine(f"sqlite:///{SQLITE_FILE}", echo=True)


app = create_app()