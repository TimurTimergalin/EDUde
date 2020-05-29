import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from data.student_invite import StudentInvite
from data import db_session
from data.teacher_invite import TeacherInvite


class Student(SqlAlchemyBase, SerializerMixin, UserMixin):
    """Student
    SQLAlchemy model of student"""
    __tablename__ = 'students'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    surname = Cl(sql.String(32))
    name = Cl(sql.String(32))
    email = Cl(sql.String(64), index=True, unique=True)
    hashed_password = Cl(sql.String(128),  nullable=True)
    teachers = orm.relationship('Teacher', secondary='teacher_to_student')
    class_rooms = orm.relationship('ClassRoom', secondary='student_to_class')
    users = orm.relation('User', back_populates='student')

    def __repr__(self):
        return f'{self.surname} {self.name}#{self.id}, student'

    def set_password(self, password):
        """Student.set_password
        set an encrypted password"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Student.check_password
        encrypt input password and compare it with current user's password"""
        return check_password_hash(self.hashed_password, password)

    def edit_myself(self, **kwargs):
        """Student.edit_myself
        edit the current object"""
        if not kwargs:
            return 1
        for i in kwargs:
            if i not in ['surname', 'name', 'email']:
                return 2
            setattr(self, i, kwargs[i])
        return 0

    def user_type(self):
        return Student

    def invite(self, teacher_id):
        session = db_session.create_session()
        invites = session.query(StudentInvite).filter(StudentInvite.student_id == self.id, StudentInvite == 1).all()
        for i in invites:
            if i.teacher_id == teacher_id:
                return
        invite_ = StudentInvite()
        invite_.student_id = self.id
        invite_.teacher_id = teacher_id
        session.add(invite_)
        session.commit()
