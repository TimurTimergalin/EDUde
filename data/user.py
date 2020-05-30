import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from data import db_session
import werkzeug
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from data.student import Student
from data.teacher import Teacher


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    teacher_id = Cl(sql.Integer, sql.ForeignKey('teachers.id'), nullable=True)
    teacher = orm.relation('Teacher')
    student_id = Cl(sql.Integer, sql.ForeignKey('students.id'), nullable=True)
    student = orm.relation('Student')

    def __repr__(self):
        return f'teacher: {self.teacher} id: {self.teacher_id}; student: {self.student} id:{self.student_id}'

    def get_id(self):
        return self.id

    def get_user(self):
        if self.is_teacher:
            return self.teacher
        return self.student

    def user_type(self):
        if type(self.teacher_id) == int:
            return Teacher
        return Student
