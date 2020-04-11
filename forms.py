from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from flask_wtf.recaptcha import RecaptchaField


RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'


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
    recaptcha = RecaptchaField()
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """LoginForm
    WTF model of login form"""
    email = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')




