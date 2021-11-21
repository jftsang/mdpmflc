from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, StopValidation
from wtforms.widgets import TextArea

from mdpmflc.config import DPMDRIVERS


def is_identifier(form, field):
    if not field.data.isidentifier():
        message = field.gettext('This field needs to be an identifier.')

        field.errors[:] = []
        raise StopValidation(message)



def JobSubmissionFormFactory(drivers, seriess, jobs):
    def is_unique_label_in_series(form, field):
        collisions = jobs.filter_by(label=field.data, series_id=form.series.data)
        if collisions.count():
             raise StopValidation("There is already a simulation with this label in this series")

    class JobSubmissionForm(FlaskForm):
        drivers_choices = list(map(lambda x: (x.id, x.name), drivers))
        series_choices = list(map(lambda x: (x.id, x.name), seriess))
        driver = SelectField('Driver', choices=drivers_choices)
        series = SelectField('Series', choices=series_choices)
        label = StringField('Label', validators=[
            DataRequired(), Length(2, 100), is_identifier, is_unique_label_in_series
        ])
        config = StringField('Config', widget=TextArea())
        submit = SubmitField('Queue a job')

    return JobSubmissionForm()