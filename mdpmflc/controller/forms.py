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


def JobSubmissionFormFactory(series_choices):
    class JobSubmissionForm(FlaskForm):
        driver = SelectField('Driver', choices=DPMDRIVERS)
        series = SelectField('Series', choices=series_choices)
        label = StringField('Label', validators=[
            DataRequired(), Length(2, 100), is_identifier
        ])
        config = StringField('Config', widget=TextArea())
        submit = SubmitField('Queue a job')

    return JobSubmissionForm()