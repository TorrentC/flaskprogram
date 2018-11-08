from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    number = StringField('学号', validators=[DataRequired()])
    name = StringField('姓名', validators=[DataRequired()])
    submit = SubmitField('提交')


class ChooseForm(FlaskForm):
    pass