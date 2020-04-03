import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase


teacher_to_subject = sql.Table('teacher_to_subject', SqlAlchemyBase.metadata,
                               Cl('teacher', sql.Integer, sql.ForeignKey('teachers.id')),
                               Cl('subject', sql.Integer, sql.ForeignKey('subjects.id')))

teacher_to_student = sql.Table('teacher_to_student', SqlAlchemyBase.metadata,
                               Cl('teacher', sql.Integer, sql.ForeignKey('teachers.id')),
                               Cl('student', sql.Integer, sql.ForeignKey('students.id')))


class Teacher(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    surname = Cl(sql.String)
    name = Cl(sql.String)
    subjects = orm.relationship('Subject', secondary='teacher_to_subject')
    students = orm.relationship('Student', secondary='teacher_to_student')
    class_rooms = orm.relation('ClassRoom', back_populates='teacher')

    def __repr__(self):
        return f'{self.surname} {self.name}, учитель'

    def add_student(self, student):
        self.students.append(student)

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_class(self, class_room):
        self.class_rooms.append(class_room)
