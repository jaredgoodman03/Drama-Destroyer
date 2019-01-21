from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	ranking = StringField('Ranking', validators=[DataRequired()])
	submit = SubmitField('Submit')
