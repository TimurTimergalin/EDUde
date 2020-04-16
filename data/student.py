import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


student_to_class = sql.Table('student_to_class', SqlAlchemyBase.metadata,
                             Cl('student', sql.Integer, sql.ForeignKey('students.id')),
                             Cl('class_room', sql.Integer, sql.ForeignKey('class_rooms.id')))


class Student(SqlAlchemyBase, SerializerMixin, UserMixin):
    """Student
    SQLAlchemy model of student"""
    __tablename__ = 'students'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    surname = Cl(sql.String)
    name = Cl(sql.String)
    email = Cl(sql.String, index=True, unique=True)
    hashed_password = Cl(sql.String,  nullable=True)
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
            if i not in ['surname', 'name']:
                return 2
            setattr(self, i, kwargs[i])
        return 0

    def user_type(self):
        return Student
