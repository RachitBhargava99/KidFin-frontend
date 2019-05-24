from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email


class AddRecruiterForm(FlaskForm):
    name = StringField('Recruiter Name', validators=[DataRequired()])
    submit = SubmitField('Submit')
