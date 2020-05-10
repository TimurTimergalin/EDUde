from click import DateTime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, TextAreaField, DateTimeField, DateField, TimeField, FileField
from wtforms.fields.html5 import EmailField, DateTimeLocalField
from wtforms.validators import DataRequired
from flask_wtf.recaptcha import RecaptchaField
from datetime import datetime

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
    email = EmailField('Эл. почта', validators=[DataRequired()])
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
    pass


class EditProfile(FlaskForm):
    """EditProfile
       WTF model of Edit profile form"""
    new_name = StringField('Имя', validators=[DataRequired()])
    new_surname = StringField('Фамилия', validators=[DataRequired()])
    new_email = EmailField('Логин', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class EditClass(FlaskForm):
    """EditClass
       WTF model of Edit class form"""
    new_name = StringField('Название', validators=[DataRequired()])
    new_subject = StringField('Предмет', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


def new_edit_task(task):
    class EditTask(FlaskForm):
        """EditTask
           WTF model of Edit task form"""
        new_name = StringField('Название задания', validators=[DataRequired()], default=task.name)
        new_description = TextAreaField('Что делать', validators=[DataRequired()], default=task.description)
        new_deadline = DateTimeLocalField("Дедлайн", validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
                                     default=task.deadline)
        new_link = StringField('Куда отправлять', validators=[DataRequired()], default=task.link)
        submit = SubmitField('Отправить')
    return EditTask()
