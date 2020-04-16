import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data import db_session
from data.db_session import SqlAlchemyBase
import werkzeug
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


# Таблица для отношения учитель-предмет
teacher_to_subject = sql.Table('teacher_to_subject', SqlAlchemyBase.metadata,
                               Cl('teacher', sql.Integer, sql.ForeignKey('teachers.id')),
                               Cl('subject', sql.Integer, sql.ForeignKey('subjects.id')))

# Таблица для отношения учитель-студент
teacher_to_student = sql.Table('teacher_to_student', SqlAlchemyBase.metadata,
                               Cl('teacher', sql.Integer, sql.ForeignKey('teachers.id')),
                               Cl('student', sql.Integer, sql.ForeignKey('students.id')))


class Teacher(SqlAlchemyBase, SerializerMixin, UserMixin):
    """Teacher
    SQLAlchemy model of teacher"""
    __tablename__ = 'teachers'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    surname = Cl(sql.String)
    name = Cl(sql.String)
    email = Cl(sql.String, index=True, unique=True)
    hashed_password = Cl(sql.String,  nullable=True)
    subjects = orm.relationship('Subject', secondary='teacher_to_subject')
    students = orm.relationship('Student', secondary='teacher_to_student')
    class_rooms = orm.relation('ClassRoom', back_populates='teacher')
    users = orm.relation('User', back_populates='teacher')

    def __repr__(self):
        return f'{self.surname} {self.name}#{self.id}, teacher'

    def add_student(self, student):
        """Teacher.add_student
        add a student to the current teacher's students list"""
        try:
            self.students.append(student)
            return 0
        except Exception:
            return 1

    def remove_student(self, student):
        """Teacher.remove_student
        remove a student from the current teacher's students list"""
        try:
            self.students.remove(student)
            return 0
        except Exception:
            return 1

    def add_subject(self, subject):
        """Teacher.add_subject
        add a subject to the current teacher's subjects list"""
        try:
            self.subjects.append(subject)
            return 0
        except Exception:
            return 0

    def remove_subject(self, subject):
        """Teacher.remove_subject
        remove a subject from the current teacher's subjects list"""
        try:
            self.subjects.remove(subject)
            return 0
        except Exception:
            return 0

    def add_class(self, class_room, subject):
        """Teacher.add_class
        add a classroom to the current teacher's classrooms list"""
        try:
            class_room.set_subject(subject)
            class_room.teacher = self
            self.class_rooms.append(class_room)
            return 0
        except Exception:
            return 1

    def remove_class(self, class_room):
        """Teacher.remove_class
        delete class_room"""
        try:
            session = db_session.create_session()
            session.delete(class_room)
            return 0
        except Exception:
            return 1

    def set_password(self, password):
        """Teacher.set_password
        set an encrypted password"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Teacher.check_password
        encrypt input password and compare it with current user's password"""
        return check_password_hash(self.hashed_password, password)

    def edit_myself(self, **kwargs):
        """Teacher.edit_myself
        edit the current object"""
        if not kwargs:
            return 1
        for i in kwargs:
            if i not in ['surname', 'name']:
                return 2
            setattr(self, i, kwargs[i])
        return 0

    def user_type(self):
        return Teacher

