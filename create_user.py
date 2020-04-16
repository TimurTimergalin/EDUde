import sys
sys.path.insert(1, '/data')
from data import db_session
from data.user import User
from data.teacher import Teacher
from data.student import Student


def create_user(**kw):
    base_user = User()
    if kw['user_type'] == Teacher:
        user = Teacher()
        base_user.teacher = user
        base_user.is_teacher = 1
    else:
        user = Student()
        base_user.student = user
        base_user.is_teacher = 0
    user.surname = kw['surname']
    user.name = kw['name']
    user.email = kw['email']
    user.set_password(kw['password'])
    session = db_session.create_session()
    session.add(base_user)
    session.add(user)
    session.commit()
