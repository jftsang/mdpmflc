from flask_sqlalchemy import SQLAlchemy

from mdpmflc.app import create_app

db = SQLAlchemy(create_app())

class Job(db.Model):
    id = db.Column('job_id', db.Integer, primary_key=True)
    driver = db.Column(db.String(100))
    series = db.Column(db.String(100))
    label = db.Column(db.String(100))
    config = db.Column(db.Text)
    status = db.Column(db.Integer)

    def __init__(self, driver, series, label, config, status):
        self.driver = driver
        self.series = series
        self.label = label
        self.config = config
        self.status = status
