import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
import werkzeug


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
    hashed_password = Cl(sql.String,  nullable=True)
    subjects = orm.relationship('Subject', secondary='teacher_to_subject')
    students = orm.relationship('Student', secondary='teacher_to_student')
    class_rooms = orm.relation('ClassRoom', back_populates='teacher')

    def __repr__(self):
        return f'{self.surname} {self.name}#{self.id}, учитель'

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

    def add_subject(self, subject):
        try:
            self.subjects.append(subject)
            return 0
        except Exception:
            return 0

    def remove_subject(self, subject):
        try:
            self.subjects.remove(subject)
            return 0
        except Exception:
            return 0

    def add_class(self, class_room, subject):
        try:
            class_room.set_subject(subject)
            class_room.teacher = self
            self.class_rooms.append(class_room)
            return 0
        except Exception:
            return 1

    def set_password(self, password):
        self.hashed_password = werkzeug.generate_password_hash(password)

    def check_password(self, password):
        return werkzeug.check_password_hash(self.hashed_password, password)

    def edit_myself(self, **kwargs):
        if not kwargs:
            return 1
        for i in kwargs:
            if i not in ['surname', 'name']:
                return 2
            setattr(self, i, kwargs[i])
        return 0

