import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm
from data import db_session
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from data.student_to_class import StudentToClass


class ClassRoom(SqlAlchemyBase, SerializerMixin):
    """ClassRoom
    SQLAlchemy model of classroom"""
    __tablename__ = 'class_rooms'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    name = Cl(sql.String)
    teacher_id = Cl(sql.Integer, sql.ForeignKey('teachers.id'))
    teacher = orm.relation('Teacher')
    students = orm.relationship('Student', secondary='student_to_class')
    subject = Cl(sql.String)
    tasks = orm.relation('Task', back_populates='class_room')

    def __repr__(self):
        return f'Class \'{self.name}\'#{self.id}'

    def add_student(self, student):
        """ClassRoom.add_student
        add student to the current class' students list"""
        try:
            if student in self.students:
                return 1
            session = db_session.create_session()
            relation = StudentToClass()
            relation.student_id = student.id
            relation.classroom_id = self.id
            session.add(relation)
            session.commit()

            return 0
        except Exception:
            return 1

    def remove_student(self, student):
        """ClassRoom.remove_student
        remove student from the current class' students list"""
        try:
            if student not in self.students:
                return 1
            session = db_session.create_session()
            relation = session.query(StudentToClass).filter(StudentToClass.student_id == student.id,
                                                            StudentToClass.classroom_id == self.id).first()
            session.delete(relation)
            session.commit()
            return 0
        except Exception:
            return 1

    def add_task(self, task):
        """ClassRoom.add_task
        add task to the current class' tasks list"""
        try:
            if task in self.tasks:
                return 1
            task.class_room = self
            self.tasks.append(task)
            return 0
        except Exception:
            return 1

    def remove_task(self, task):
        """ClassRoom.remove_task
        remove task from the current class' tasks list"""
        try:
            if task not in self.tasks:
                return 1
            session = db_session.create_session()
            session.delete(task)
            return 0
        except Exception:
            return 1

    def edit_myself(self, **kwargs):
        """ClassRoom.edit_myself
        edit the current object"""
        if not kwargs:
            return 1
        for i in kwargs:
            if i != 'name':
                return 2
            setattr(self, i, kwargs[i])
        return 0
