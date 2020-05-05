from click import DateTime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, TextAreaField, DateTimeField, DateField, TimeField, FileField
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
    # recaptcha = RecaptchaField()
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    """LoginForm
    WTF model of login form"""
    email = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddClassForm(FlaskForm):
    """AddClassForm
       WTF model of Add class form"""
    name_of_class = StringField('Название класса', validators=[DataRequired()])
    subj = StringField('Предмет', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class AddTaskForm(FlaskForm):
    """AddTaskForm
       WTF model of Add class form"""
    name_of_task = TextAreaField('Название задания', validators=[DataRequired()])
    task = TextAreaField('Что делать', validators=[DataRequired()])
    deadline = DateTimeField("Дедлайн", validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    link = StringField('Куда отправлять', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class InvitingForm(FlaskForm):
    """invitingForm
       WTF model of Inviting form"""
    id = StringField('Введите id пользователя', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class AcceptionForm(FlaskForm):
    submit_true = SubmitField('Удалить')


class SendHomework(FlaskForm):
    """SendHomework
       WTF model of send homework form"""
    file = FileField('', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class EditProfile(FlaskForm):
    """EditProfile
       WTF model of Edit profile form"""
    new_name = StringField('Имя', validators=[DataRequired()])
    new_surname = StringField('Фамилия', validators=[DataRequired()])
    new_email = EmailField('Логин', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
