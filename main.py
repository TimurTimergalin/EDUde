import sys

from flask_login import LoginManager, login_user
from werkzeug.utils import redirect
from create_user import create_user

sys.path.insert(1, '/data')
from flask import Flask, render_template
from data import db_session
from data.student import Student
from data.teacher import Teacher
from data.user import User
from create_user import create_user
from flask_restful import Api
from forms import RegistrationForm, LoginForm
import student_resources
import teacher_resources
import classroom_resources
import task_resources

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(student_resources.StudentResource, '/api/1.0/student/<int:id>')
api.add_resource(student_resources.StudentListResource, '/api/1.0/student')
api.add_resource(teacher_resources.TeacherResource, '/api/1.0/teacher/<int:id>')
api.add_resource(teacher_resources.TeacherListResource, '/api/1.0/teacher')
api.add_resource(classroom_resources.ClassRoomResource,
                 '/api/1.0/classroom/<int:teacher_id>/<int:teacher_password>/<int:class_room_id>')
api.add_resource(classroom_resources.ClassRoomListResource,
                 '/api/1.0/classroom/<int:teacher_id>/<int:teacher_password>')
api.add_resource(task_resources.TaskResource, '/api/task/<int:teacher_id>/<string:teacher_password>/<int:task_id>')
api.add_resource(task_resources.TaskListResource, '/api/task/<int:teacher_id>/<string:teacher_password>')


RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def start():
    return render_template('main_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(Student).filter(Student.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('log_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('log_in.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.check_password.data:
            return render_template('log_up.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # db_session.global_init('')
        session = db_session.create_session()
        if form.user_type.data == 'ученик':
            check_email(Student, session, form)
            create_user(user_type=Student, surname=form.surname.data, name=form.name.data, email=form.email.data,
                        password=form.password.data)
        elif form.user_type.data == 'учитель':
            check_email(Teacher, session, form)
            create_user(user_type=Teacher, surname=form.surname.data, name=form.name.data, email=form.email.data,
                        password=form.password.data)
        return redirect('/login')
    return render_template('log_up.html', title='Регистрация', form=form)

def check_email(user_type, session, form):
    if session.query(user_type).filter(user_type.email == form.email.data).first():
        return render_template('log_up.html', title='Регистрация',
                               form=form,
                               message="Такой пользователь уже есть")


def main():
    db_session.global_init("db/edu.sqlite")
    session = db_session.create_session()
    app.run()


if __name__ == '__main__':
    main()
