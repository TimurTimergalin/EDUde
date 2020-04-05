import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class ClassRoom(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'class_rooms'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    name = Cl(sql.Integer)
    subject_id = Cl(sql.Integer, sql.ForeignKey('subjects.id'))
    subject = orm.relation('Subject')
    teacher_id = Cl(sql.Integer, sql.ForeignKey('teachers.id'))
    teacher = orm.relation('Teacher')
    students = orm.relationship('Student', secondary='student_to_class')
    tasks = orm.relation('Task', back_populates='class_room')

    def __repr__(self):
        return f'Class \'{self.name}\'#{self.id}'

    def add_student(self, student):
        try:
            self.students.append(student)
            return 0
        except Exception:
            return 1

    def remove_student(self, student):
        try:
            self.students.remove(student)
            return 0
        except Exception:
            return 1

    def set_subject(self, subject):
        try:
            self.subject = subject
            return 0
        except Exception:
            return 1

    def add_task(self, task):
        try:
            task.class_room = self
            self.tasks.append(task)
            return 0
        except Exception:
            return 1

    def edit_myself(self, **kwargs):
        if not kwargs:
            return 1
        for i in kwargs:
            if i != 'name':
                return 2
            setattr(self, i, kwargs[i])
        return 0
