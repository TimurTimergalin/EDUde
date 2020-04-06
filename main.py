import sys

from flask_login import LoginManager
from sqlalchemy.testing.pickleable import User
from werkzeug.utils import redirect
from create_user import create_user

sys.path.insert(1, '/data')
from flask import Flask, render_template
from data import db_session
from data.student import Student
from data.teacher import Teacher
from flask_restful import Api
from forms import RegistrationForm, LoginForm
import student_resources
import teacher_resources
import classroom_resources


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(student_resources.StudentResource, '/api/1.0/students/<int:id>')
api.add_resource(student_resources.StudentListResource, '/api/1.0/students')
api.add_resource(teacher_resources.TeacherResource, '/api/1.0/teacher/<int:id>')
api.add_resource(teacher_resources.TeacherListResource, '/api/1.0/teacher')
api.add_resource(classroom_resources.ClassRoomResource,
                 '/api/1.0/classroom/<int:teacher_id>/<int:teacher_password>/<int:class_room_id>')
api.add_resource(classroom_resources.ClassRoomListResource,
                 '/api/1.0/classroom/<int:teacher_id>/<int:teacher_password>')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/start')
def start():
    return render_template('main_page.html')


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('log_in.html', title='Вход', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.check_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        # db_session.global_init('')
        session = db_session.create_session()
        if form.user_type == 'ученик':
            check_email(Student, session, form)
            registration_finale(Student, session, form)
        elif form.user_type == 'учитель':
            check_email(Teacher, session, form)
            registration_finale(Teacher, session, form)
        return redirect('/login')
    return render_template('log_up.html', title='Регистрация', form=form)

def check_email(user_type, session, form):
    if session.query(user_type).filter(user_type.email == form.email.data).first():
        return render_template('register.html', title='Регистрация',
                               form=form,
                               message="Такой пользователь уже есть")


def registration_finale(user_type, session, form):
    user = user_type(
        surname=form.surname.data,
        name=form.name.data,
        email=form.email.data,
        type=form.user_type.data
    )
    user.set_password(form.password.data)
    session.add(user)
    session.commit()


def main():
    db_session.global_init("db/edu.sqlite")
    session = db_session.create_session()
    app.run()


if __name__ == '__main__':
    main()
