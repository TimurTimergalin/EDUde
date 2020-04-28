import sys

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect
from create_user import create_user

sys.path.insert(1, '/data')
from flask import Flask, render_template
from data import db_session
from data.student import Student
from data.teacher import Teacher
from data.class_room import ClassRoom
from data.user import User
from create_user import create_user
from flask_restful import Api
from forms import RegistrationForm, LoginForm, RECAPTCHA_PRIVATE_KEY, RECAPTCHA_PUBLIC_KEY, AddClassForm
import student_resources
import teacher_resources
import classroom_resources
import task_resources
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(filename='logs/edude.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
api = Api(app)
api.add_resource(student_resources.StudentResource, '/api/1.0/student/<int:student_id>&<string:student_password>')
api.add_resource(student_resources.StudentListResource, '/api/1.0/students')
api.add_resource(student_resources.StudentGetResource, '/api/1.0/student/<int:student_id>')
api.add_resource(teacher_resources.TeacherGetResource, '/api/1.0/teacher/<int:teacher_id>')
api.add_resource(teacher_resources.TeacherResource, '/api/1.0/teacher/<int:teacher_id>&<string:teacher_password>')
api.add_resource(teacher_resources.TeacherListResource, '/api/1.0/teachers')
api.add_resource(classroom_resources.ClassRoomResource,
                 '/api/1.0/classroom/<int:teacher_id>&<string:teacher_password>&<int:class_room_id>')
api.add_resource(classroom_resources.ClassRoomListResource,
                 '/api/1.0/classrooms/<int:teacher_id>&<string:teacher_password>')
api.add_resource(task_resources.TaskResource, '/api/1.0/task/<int:teacher_id>&<string:teacher_password>&<int:task_id>')
api.add_resource(task_resources.TaskListResource, '/api/1.0/tasks/<int:teacher_id>&<string:teacher_password>')

RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'


def log_func(func):
    def new_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as ex:
            logging.error(f":error in {func.__name__}: {', '.join(ex.args)}")
        else:
            logging.info(f':The result of {func.__name__} is: {result}')
            return result
    return new_func


@app.errorhandler(403)
def error403(e):
    return redirect('bad_request.html')


@app.errorhandler(401)
def error401(e):
    return redirect('/login')


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
        user = user_type_choice(session, form)
        if user and user.check_password(form.password.data):
            login_user(user.users[0], remember=form.remember_me.data)
            return redirect("/profile")
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
        if check_email(session, form):
            if form.user_type.data == 'ученик':
                create_user(user_type=Student, surname=form.surname.data, name=form.name.data, email=form.email.data,
                            password=form.password.data)
            elif form.user_type.data == 'учитель':
                create_user(user_type=Teacher, surname=form.surname.data, name=form.name.data, email=form.email.data,
                            password=form.password.data)
        else:
            return render_template('log_up.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        return redirect('/logup_successful')
    return render_template('log_up.html', title='Регистрация', form=form)


@app.route('/logup_successful')
def logup_successful():
    return render_template('good_request.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    session = db_session.create_session()
    if current_user.user_type() == Teacher:
        form = AddClassForm()
        if form.validate_on_submit():
            if session.query(ClassRoom).filter(ClassRoom.name == form.name_of_class.data).first():
                return render_template('profile_of_teacher.html', form=form,
                                       message="Такой класс уже есть")
            classroom = ClassRoom()
            classroom.name = form.name_of_class.data
            classroom.teacher_id = current_user.teacher_id
            session.add(classroom)
            session.commit()
            redirect('/dashboard')
        print(session.query(ClassRoom).filter(
            ClassRoom.teacher_id == current_user.teacher_id))
        teacher = session.query(Teacher).filter(Teacher.id == current_user.teacher_id).first()
        return render_template('profile_of_teacher.html', form=form, classrooms=session.query(ClassRoom).filter(
            ClassRoom.teacher_id == teacher.id), name=teacher.name)
    else:
        return render_template('profile_of_student.html')


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    session = db_session.create_session()
    if current_user.user_type() == Teacher:
        teacher = session.query(Teacher).filter(Teacher.id == current_user.teacher_id).first()
        return render_template('dashboard_of_teacher.html', classrooms=session.query(ClassRoom).filter(
            ClassRoom.teacher_id == teacher.id))
    else:
        return render_template('profile_of_student.html')


@app.route('/tasks/<teacher_id>/<classroom_id>', methods=['GET', 'POST'])
@login_required
def tasks(teacher_id, classroom_id):
    if current_user.teacher_id == int(teacher_id):
        return render_template('dash_of_current_class.html', teacher_id=current_user.teacher_id,
                               classroom_id=classroom_id)
    return render_template('bad_request.html')


@app.route('/api')
def api():
    return render_template('api.html', title='Api проекта')


@app.route('/new_task')
@login_required
def new_task():
    return render_template('new_task.html', current_user=current_user)


def check_email(session, form):
    if session.query(Teacher).filter(Teacher.email == form.email.data).first():
        return True
    elif session.query(Student).filter(Student.email == form.email.data).first():
        return False
    return True


def user_type_choice(session, form):
    if session.query(Student).filter(Student.email == form.email.data).first():
        return session.query(Student).filter(Student.email == form.email.data).first()
    return session.query(Teacher).filter(Teacher.email == form.email.data).first()


def main():
    db_session.global_init("db/edu.sqlite")
    session = db_session.create_session()
    app.run()


if __name__ == '__main__':
    main()
