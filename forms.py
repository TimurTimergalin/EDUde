from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    """RegistrationForm
    WTF model of registration form"""
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Эл. почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    check_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    user_type = RadioField('Учитель/Ученик', validators=[DataRequired()],
                            choices=[('учитель', 'Учитель'), ('ученик', 'Ученик')])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    """LoginForm
    WTF model of login form"""
    email = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')




