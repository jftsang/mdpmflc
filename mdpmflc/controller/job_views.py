import logging

import flask
from flask import render_template, Blueprint

from mdpmflc.config import DPMDRIVERS
from mdpmflc.controller.forms import JobSubmissionFormFactory
from mdpmflc.models import Job, Series
from mdpmflc.utils.jobs import queue_job, start_job
from mdpmflc.utils.listings import get_available_series

logging.getLogger().setLevel(logging.INFO)

job_views = Blueprint('job_views', __name__)


@job_views.route("/index")
def job_index_view():
    queue = Job.query.all()
    return render_template("jobs/job_queue.html",
                           queue=queue)


@job_views.route("/queue", methods=["GET", "POST"])
def queue_job_view():
    """Receive a request for a simulation and queue it."""
    series_choices = list(map(lambda x: (x.id, x.name), Series.query.all()))
    form = JobSubmissionFormFactory(series_choices)

    if form.validate_on_submit():
        # https://code.luasoftware.com/tutorials/flask/flask-get-request-parameters-get-post-and-json/
        logging.info(f"Received a job request for {form.driver.data}, {form.series.data}/{form.label.data}")

        queue_job(
            form.driver.data, form.series.data, form.label.data, form.config.data
        )

        # return pformat(dir(flask.request.form))
        # return f"Started a run of driver {driver} on series {sername}, simulation name {simname}"
        # return Response(flask.request.get_json(), mimetype="application/json")
        series_name = Series.query.get(form.series.data).name
        return render_template("jobs/successful_queue.html",
                               hostname=flask.request.host,
                               driver=form.driver.data,
                               sername=series_name,
                               simname=form.label.data)

    return render_template("jobs/queue_form.html",
                           drivers=DPMDRIVERS,
                           series=get_available_series(),
                           form=form)


@job_views.route("/start/<job_id>", methods=["GET", "POST"])
def start_job_controller(job_id):
    start_job(job_id)