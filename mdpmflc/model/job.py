from mdpmflc.model import db


class Job(db.Model):
    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    driver = db.Column(db.String(100))
    series = db.Column(db.String(100))
    label = db.Column(db.String(100), nullable=False)
    config = db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, driver, series, label, config, status):
        self.driver = driver
        self.series = series
        self.label = label
        self.config = config
        self.status = status
