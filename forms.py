from click import DateTime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, TextAreaField, DateTimeField, DateField, TimeField, FileField
from wtforms.fields.html5 import EmailField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from flask_wtf.recaptcha import RecaptchaField
from datetime import datetime

RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'


class RegistrationForm(FlaskForm):
    """RegistrationForm
    WTF model of registration form"""
    surname = StringField('Фамилия', validators=[DataRequired(), Length(max=32)])
    name = StringField('Имя', validators=[DataRequired(), Length(max=32)])
    email = EmailField('Эл. почта', validators=[DataRequired(), Length(max=64)])
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
    name_of_class = StringField('Название класса', validators=[DataRequired(), Length(1, 32)])
    subj = StringField('Предмет', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField('Сохранить')


class AddTaskForm(FlaskForm):
    """AddTaskForm
       WTF model of Add class form"""
    task = TextAreaField('Что делать', validators=[DataRequired()])
    name_of_task = StringField('Название задания', validators=[DataRequired(), Length(1, 32)])
    link = StringField('Куда отправлять', validators=[DataRequired(), Length(1, 128)])
    deadline = DateTimeField("Дедлайн", validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Отправить')


class AddFormTaskForm(FlaskForm):
    name_of_task = TextAreaField('Название задания', validators=[DataRequired(), Length(1, 32)])
    form_link = StringField('Ссылка на Google Форму', validators=[DataRequired(), Length(1, 128)])
    link = StringField('Куда отправлять', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Отправить')


class InvitingForm(FlaskForm):
    """invitingForm
       WTF model of Inviting form"""
    id = StringField('Введите id пользователя', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


class SendHomework(FlaskForm):
    pass


class AcceptionForm(FlaskForm):
    submit_true = SubmitField('Удалить')


class EditProfile(FlaskForm):
    """EditProfile
       WTF model of Edit profile form"""
    new_name = StringField('Имя', validators=[DataRequired(), Length(1, 32)])
    new_surname = StringField('Фамилия', validators=[DataRequired(), Length(1, 32)])
    new_email = EmailField('Логин', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Сохранить')


class EditClass(FlaskForm):
    """EditClass
       WTF model of Edit class form"""
    new_name = StringField('Название', validators=[DataRequired(), Length(1, 32)])
    new_subject = StringField('Предмет', validators=[DataRequired(), Length(1, 32)])
    submit = SubmitField('Сохранить')


def new_edit_task(task, normal_task):
    class EditTask(FlaskForm):
        """EditTask
           WTF model of Edit task form"""
        new_name = StringField('Название задания', validators=[DataRequired(), Length(1, 32)], default=task.name)
        new_description = TextAreaField('Что делать', validators=[DataRequired()], default=normal_task.description)
        new_deadline = DateTimeLocalField("Дедлайн", validators=[DataRequired()], format='%Y-%m-%dT%H:%M',
                                     default=task.deadline)
        new_link = StringField('Куда отправлять', validators=[DataRequired(), Length(1, 128)], default=task.link)
        submit = SubmitField('Отправить')
    return EditTask()
