import sys

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect
from create_user import create_user

sys.path.insert(1, '/data')
from flask import Flask, render_template, url_for, request
from data import db_session
from data.student import Student
from data.teacher import Teacher
from data.class_room import ClassRoom
from data.user import User
from data.task import Task
from create_user import create_user
from flask_restful import Api
from api_func import *
from data.student_invite import StudentInvite
from data.teacher_invite import TeacherInvite
from data.student_to_class import StudentToClass
from forms import *
import student_resources
import teacher_resources
import classroom_resources
import task_resources
from email_sender import sendmessage
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# logging.basicConfig(filename='logs/edude.log', level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(name)s %(message)s')

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


@app.errorhandler(404)
def error404(e):
    return render_template('not_found.html')


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
        teacher = session.query(Teacher).filter(Teacher.id == current_user.teacher_id).first()
        return render_template('profile_of_teacher.html', classrooms=session.query(ClassRoom).filter(
            ClassRoom.teacher_id == teacher.id), name=teacher.name, id=teacher.id,
                               students=teacher.students, surname=teacher.surname, is_teacher=True,
                               invites=session.query(StudentInvite).filter(StudentInvite.teacher == teacher).all())
    else:
        student = session.query(Student).filter(Student.id == current_user.student_id).first()
        return render_template('profile_of_student.html', classrooms=student.class_rooms,
                               name=student.name, id=student.id, surname=student.surname, is_teacher=False,
                               invites=session.query(TeacherInvite).filter(TeacherInvite.student == student).all())


@app.route('/new_student/<classroom_id>', methods=["GET", "POST"])
@login_required
def new_student(classroom_id):
    if current_user.user_type() == Teacher:
        if request.method == 'GET':
            return render_template('add_students.html', students=current_user.teacher.students)
        elif request.method == 'POST':
            session = db_session.create_session()
            classroom = session.query(ClassRoom).get(classroom_id)
            for data in request.form.getlist('checkbox'):
                student = session.query(Student).get(int(data))
                classroom.add_student(student)
            session.commit()
        return redirect(f'/tasks/{classroom_id}')
    return redirect('/profile')


@app.route('/new_class', methods=["GET", "POST"])
@login_required
def add_class():
    form = AddClassForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if session.query(ClassRoom).filter(ClassRoom.name == form.name_of_class.data,
                                           ClassRoom.teacher_id == current_user.teacher_id).first():
            form = AddClassForm()
            return render_template('add_class.html', form=form,
                                   message="Такой класс уже есть")
        classroom = ClassRoom()
        classroom.name = form.name_of_class.data
        classroom.subject = form.subj.data
        classroom.teacher_id = current_user.teacher_id
        session.add(classroom)
        session.commit()
        return redirect('/profile')
    return render_template('add_class.html', form=form)


# chego blin
@app.route('/tasks/<classroom_id>', methods=['GET', 'POST'])
@login_required
def tasks(classroom_id):
    session = db_session.create_session()
    deadline_delete(classroom_id)
    classroom = session.query(ClassRoom).get(classroom_id)
    students = classroom.students
    if current_user.user_type() == Teacher:
        if session.query(ClassRoom).get(classroom_id).teacher_id == current_user.teacher_id:
            return render_template('dash_of_current_class.html',
                                   classroom_id=classroom_id, link_css=url_for('static', filename='css/table.css'),
                                   link_css1=url_for('static', filename='css/tasks.css'),
                                   link_css2=url_for('static', filename='css/dash_of_cur_cl.css'),
                                   link_logo=url_for('static', filename='img/logo.png'),
                                   tasks=session.query(Task).filter(
                                       Task.class_room_id == classroom_id), is_teacher=True, students=students)
    else:
        student = session.query(Student).get(current_user.student_id)
        if student in session.query(ClassRoom).get(classroom_id).students:
            return render_template('dash_of_current_class.html',
                                   classroom_id=classroom_id, link_css=url_for('static', filename='css/table.css'),
                                   link_css1=url_for('static', filename='css/tasks.css'),
                                   link_css2=url_for('static', filename='css/dash_of_cur_cl.css'),
                                   link_logo=url_for('static', filename='img/logo.png'),
                                   tasks=session.query(Task).filter(
                                       Task.class_room_id == classroom_id), is_teacher=False)
    return render_template('bad_request.html')


@app.route('/kek/<int:task_id>', methods=['GET', 'POST'])
@login_required
def kek(task_id):
    if abort_if_request_is_forbidden1(current_user.teacher_id, task_id):
        if request.method == 'GET':
            return render_template('kek.html', task_id=task_id)
        elif request.method == 'POST':
            session = db_session.create_session()
            task = session.query(Task).get(task_id)
            session.delete(task)
            session.commit()
            return redirect('/profile')


@app.route('/accept_invite/<int:invite_id>')
@login_required
def accept_invite(invite_id):
    session = db_session.create_session()
    if current_user.user_type() == Teacher:
        invite_ = session.query(StudentInvite).get(invite_id)
        if invite_.teacher == current_user.teacher:
            current_user.teacher.add_student(invite_.student)
    else:
        invite_ = session.query(TeacherInvite).get(invite_id)
        if invite_.student == current_user.student:
            invite_.teacher.add_student(current_user.student)
    session.delete(invite_)
    session.commit()
    return redirect('/profile')


@app.route('/refuse_invite/<int:invite_id>')
@login_required
def refuse_invite(invite_id):
    session = db_session.create_session()
    if current_user.user_type() == Teacher:
        invite_ = session.query(StudentInvite).get(invite_id)
        if invite_.teacher != current_user.teacher:
            return redirect('/profile')
    else:
        invite_ = session.query(TeacherInvite).get(invite_id)
        if invite_.student != current_user.student:
            return redirect('/profile')
    session.delete(invite_)
    session.commit()
    return redirect('/profile')


@app.route('/api')
def api():
    return render_template('api.html', title='API проекта')


@app.route('/api/1.0')
def api_1_0():
    return render_template('documentation_1.0.html', title='API v1.0')
    # form = AddClassForm()/


@app.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    form = InvitingForm()
    if form.validate_on_submit():
        if current_user.user_type() == Teacher:
            user = current_user.teacher
            for i in user.students:
                if i.id == int(form.id.data):
                    return redirect('/profile')
            abort_if_student_not_found(int(form.id.data))
            user.invite(int(form.id.data))
        else:
            user = current_user.student
            for i in user.teachers:
                if i.id == int(form.id.data):
                    return redirect('/profile')
            abort_if_teacher_not_found(int(form.id.data))
            user.invite(int(form.id.data))
        return redirect('/profile')
    return render_template('invitings.html', form=form)


@app.route('/send_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def send_task(task_id):
    if current_user.user_type() == Teacher:
        return redirect('/profile')
    abort_if_task_not_found(task_id)
    form = SendHomework()
    session = db_session.create_session()
    task = session.query(Task).get(task_id)
    classroom = task.class_room
    student = session.query(Student).get(current_user.student_id)
    if request.method == 'GET':
        if current_user.user_type() == Student:
            if student in classroom.students:
                return render_template('send_homework.html', form=form)
        return redirect('/profile')
    elif request.method == 'POST':
        # text = request.form['message']
        files = request.files
        i = 1
        files_list = []
        while True:
            try:
                files_list.append(request.files[str(i)].read())
                i += 1
            except Exception:
                break
        a = [str(file[1]).split()[2][2:-3].split('/') for file in files.items()]
        b = [i for i in files_list]
        c = [a[i] + [b[i]] for i in range(len(a))]
        sendmessage(student.surname, classroom.name, task.name, task.link, request.form['text'], c)
        return redirect('/profile')


@app.route('/new_task/<classroom_id>', methods=['GET', 'POST'])
@login_required
def new_task(classroom_id):
    abort_if_class_not_found(classroom_id)
    if current_user.user_type() == Teacher:
        form = AddTaskForm()
        session = db_session.create_session()
        if form.validate_on_submit():
            task = Task()
            task.name = form.name_of_task.data
            task.description = form.task.data
            task.link = form.link.data
            task.teacher_id = current_user.teacher_id
            task.deadline = form.deadline.data
            task.class_room_id = classroom_id
            session.add(task)
            session.commit()
            return redirect(f'/tasks/{classroom_id}')
        return render_template('new_task.html', current_user=current_user,
                               classrooms=session.query(ClassRoom).filter(
                                   ClassRoom.teacher_id == current_user.teacher_id),
                               form=form)


@app.route('/delete_student/<int:classroom_id>/<int:student_id>', methods=['GET', 'POST'])
@login_required
def delete_student(classroom_id, student_id):
    abort_if_class_not_found(classroom_id)
    abort_if_student_not_found(student_id)
    if current_user.user_type() == Student:
        return redirect('/profile')
    sesssion = db_session.create_session()
    classroom = sesssion.query(ClassRoom).get(classroom_id)
    student = sesssion.query(Student).get(student_id)
    teacher = sesssion.query(Teacher).get(current_user.teacher_id)
    abort_if_request_is_forbidden(teacher.id, classroom_id)
    if student not in classroom.students:
        abort(403, message='This student is not in this classroom')
    if request.method == 'GET':
        return render_template('kek.html')
    elif request.method == 'POST':
        classroom.remove_student(student)
        return redirect(f'/tasks/{classroom_id}')


@app.route('/delete_classroom/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def delete_classroom(classroom_id):
    if current_user.user_type() == Student:
        return redirect('/profile')
    abort_if_class_not_found(classroom_id)
    session = db_session.create_session()
    classroom = session.query(ClassRoom).get(classroom_id)
    teacher = session.query(Teacher).get(current_user.teacher_id)
    abort_if_request_is_forbidden(teacher.id, classroom_id)
    if request.method == 'GET':
        return render_template('kek.html')
    elif request.method == 'POST':
        session.delete(classroom)
        session.commit()
        return redirect('/profile')


@app.route('/edit_classroom/<int:classroom_id>', methods=['GET', 'POST'])
@login_required
def edit_classroom(classroom_id):
    if current_user.user_type() == Student:
        return redirect('/profile')
    abort_if_class_not_found(classroom_id)
    form = EditClass()
    session = db_session.create_session()
    classroom = session.query(ClassRoom).get(classroom_id)
    abort_if_request_is_forbidden(current_user.teacher_id, classroom_id)
    if form.validate_on_submit():
        classroom.name = form.new_name.data
        classroom.subject = form.new_subject.data
        session.commit()
        return redirect(f'/tasks/{classroom_id}')
    return render_template('edit_class.html', classroom=classroom, form=form)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    session = db_session.create_session()
    form = EditProfile()
    current_user_html = current_user.teacher if current_user.user_type() == Teacher else current_user.student
    if form.validate_on_submit():
        edit_user = session.query(current_user.user_type()).get(current_user_html.id)
        edit_user.name = form.new_name.data
        edit_user.surname = form.new_surname.data
        edit_user.email = form.new_email.data
        session.commit()
        return redirect('/profile')
    return render_template('edit_profile.html', form=form, title='Изменить профиль', current_user=current_user_html)


def deadline_delete(classroom_id):
    session = db_session.create_session()
    tasks = session.query(ClassRoom).get(classroom_id).tasks
    for task in tasks:
        if datetime.now() > task.deadline:
            session.delete(task)
    session.commit()


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
    app.run()


if __name__ == '__main__':
    main()
