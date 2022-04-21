from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class OthersForm(FlaskForm):

    title = StringField('Имя', validators=[DataRequired()])
    age = TextAreaField("возраст")
    status = TextAreaField("Статус")
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')
