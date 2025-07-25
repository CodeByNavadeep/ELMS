from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


def no_space(form, field):
    if ' ' in field.data:
        raise ValidationError('Username should not contain spaces.')


class LeaveForm(FlaskForm):
    reason = StringField('Reason', validators=[DataRequired(), Length(min=3, max=100)])
    from_date = DateField('From Date', validators=[DataRequired()])
    to_date = DateField('To Date', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Apply Leave')
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20), no_space])
    #email=StringField('email', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Employee', 'Employee'), ('Manager', 'Manager'), ('Admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')    
