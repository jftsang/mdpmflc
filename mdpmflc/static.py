from mdpmflc import app


@app.route('/style.css')
def stylesheet():
    return app.send_static_file("style.css")


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")

