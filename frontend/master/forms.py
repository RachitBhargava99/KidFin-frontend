from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, URL


class AddCompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired()])
    rep_name = StringField('Representative Name', validators=[DataRequired()])
    rep_email = StringField('Representative Email', validators=[DataRequired(), Email()])
    num_reps = IntegerField('Number of Representatives', validators=[DataRequired()])
    website = StringField('Company Website', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


class AddCompanyAdminForm(FlaskForm):
    def __init__(self, choices, *args, **kwargs):
        super(AddCompanyAdminForm, self).__init__(*args, **kwargs)
        self.company.choices = choices

    company = SelectField('Select Company')
    name = StringField('Company Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired()])
    submit = SubmitField('Submit')
