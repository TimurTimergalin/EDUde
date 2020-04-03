import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase


student_to_class = sql.Table('student_to_class', SqlAlchemyBase.metadata,
                             Cl('student', sql.Integer, sql.ForeignKey('students.id')),
                             Cl('class_room', sql.Integer, sql.ForeignKey('class_rooms.id')))


class Student(SqlAlchemyBase):
    __tablename__ = 'students'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    surname = Cl(sql.String)
    name = Cl(sql.String)
    teachers = orm.relationship('Teacher', secondary='teacher_to_student')
    class_rooms = orm.relationship('ClassRoom', secondary='student_to_class')

    def __repr__(self):
        return f'{self.surname} {self.name}#{self.id}, student'
