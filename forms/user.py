from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    email = EmailField('e-mail', validators=[DataRequired()])
    nickname = StringField('Имя пользователя')
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_copy = PasswordField('Пароль (введите заново)', validators=[DataRequired()])
    access = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('e-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
