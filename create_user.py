import sys
sys.path.insert(1, '/data')
from data import db_session
from data.user import User
from data.teacher import Teacher
from data.student import Student


def create_user(**kw):
    base_user = User()
    if kw['user_type'] == 'учитель':
        user = Teacher()
        base_user.teacher = user
    else:
        user = Student()
        base_user.student = user
    user.surname = kw['Фамилия']
    user.name = kw['Имя']
    user.email = kw['Эл. почта']
    user.set_password(kw['Пароль'])
    session = db_session.create_session()
    session.add(base_user)
    session.add(user)
    session.commit()