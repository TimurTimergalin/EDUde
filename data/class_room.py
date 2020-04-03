import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class ClassRoom(SqlAlchemyBase):
    __tablename__ = 'class_rooms'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    name = Cl(sql.Integer)
    subject_id = Cl(sql.Integer, sql.ForeignKey('subjects.id'))
    subject = orm.relation('Subject')
    teacher_id = Cl(sql.Integer, sql.ForeignKey('teachers.id'))
    teacher = orm.relation('Teacher')
    students = orm.relationship('Student', secondary='student_to_class')

    def __repr__(self):
        return f'Class \'{self.name}\'#{self.id}'

    def add_student(self, student):
        self.students.append(student)

    def set_subject(self, subject):
        self.subject = subject
