"""Endpoints that serve plots, as PNG files."""
import io
import os

from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from mdpmflc import DPMDIR, app
from mdpmflc.utils.simulation import get_dt
from mdpmflc.utils.graphics import create_data_figure, create_ene_figure


@app.route("/results/<sername>/<simname>/<ind>/plot/png")
def showdataplot_png(sername, simname, ind):
    """A plot of a .data file, in PNG format."""
    data_fn = os.path.join(DPMDIR, sername, simname, f"{simname}.data.{ind}")

    fig = create_data_figure(data_fn, vels=get_dt(sername, simname), samplesize=10000)
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
