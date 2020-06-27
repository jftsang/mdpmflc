"""Endpoints that serve plots, or webpages that contain plots."""
import io
import os

from flask import Response, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from mdpmflc import DPMDIR, app
from mdpmflc.utils.get_dt import get_dt
from mdpmflc.utils.graphics import create_data_figure, create_ene_figure
from mdpmflc.utils.read_data_file import read_data_file


@app.route('/results/<sername>/<simname>/<ind>/')
@app.route("/results/<sername>/<simname>/<ind>/plot/")
def showdataplot(sername, simname, ind):
    """A page that contains a .data file's plot."""
    dat_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")
    dimensions, headline, time, particles = read_data_file(dat_fn)

    if dimensions == 2:
        return render_template("results/data2d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=get_dt(sername, simname),
                               headline=headline, lines=particles)

    if dimensions == 3:
        return render_template("results/data3d_plot.html",
                               sername=sername, simname=simname, ind=ind, time=time,
                               dt=get_dt(sername, simname),
                               headline=headline, lines=particles)


@app.route("/results/<sername>/<simname>/<ind>/plot/png")
def showdataplot_png(sername, simname, ind):
    """A plot of a .data file, in PNG format."""
    data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")

    fig = create_data_figure(data_fn, vels=get_dt(sername, simname), samplesize=None)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/results/<sername>/<simname>/plotene/")
def showeneplot_png(sername, simname):
    """A plot of a .ene file, in PNG format."""
    ene_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.ene")

    print(ene_fn)
    fig = create_ene_figure(ene_fn)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
