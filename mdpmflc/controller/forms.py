from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, StopValidation
from wtforms.widgets import TextArea

from mdpmflc.config import DPMDRIVERS
from mdpmflc.utils.listings import get_available_series


class IsIdentifier:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not field.data.isidentifier():
            if self.message is None:
                message = field.gettext('This field is required.')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)


class JobSubmissionForm(FlaskForm):
    driver = SelectField('Driver', choices=DPMDRIVERS)
    series = SelectField('Series', choices=get_available_series())
    label = StringField('Label', validators=[DataRequired(), Length(2, 100), IsIdentifier()])
    config = StringField('Config', widget=TextArea())
    submit = SubmitField('Queue a job')
