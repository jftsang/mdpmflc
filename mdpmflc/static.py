from mdpmflc import app
from flask import render_template

#@app.route('/js/<script>.js')
#def stylesheet():
#    return app.send_static_file(f"js/{script}.js")


@app.route('/style.css')
def stylesheet():
    return app.send_static_file("style.css")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")

