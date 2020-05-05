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
from data.teacher_invite import TeacherInvite
from data.student_invite import StudentInvite
from data.teacher_to_student import TeacherToStudent


class Teacher(SqlAlchemyBase, SerializerMixin, UserMixin):
    """Teacher
    SQLAlchemy model of teacher"""
    __tablename__ = 'teachers'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    surname = Cl(sql.String)
    name = Cl(sql.String)
    email = Cl(sql.String, index=True, unique=True)
    hashed_password = Cl(sql.String,  nullable=True)
    students = orm.relationship('Student', secondary='teacher_to_student')
    class_rooms = orm.relation('ClassRoom', back_populates='teacher')
    users = orm.relation('User', back_populates='teacher')

    def __repr__(self):
        return f'{self.surname} {self.name}#{self.id}, teacher'

    def add_student(self, student):
        """Teacher.add_student
        add a student to the current teacher's students list"""
        try:
            if student in self.students:
                return 1
            relation = TeacherToStudent()
            print(self.id, student.id)
            relation.teacher_id = self.id
            relation.student_id = student.id
            session = db_session.create_session()
            session.add(relation)
            session.commit()
            session.close()
            return 0
        except Exception:
            return 1

    def remove_student(self, student):
        """Teacher.remove_student
        remove a student from the current teacher's students list"""
        try:
            if student not in self.students:
                return 1
            session = db_session.create_session()
            relation = session.query(TeacherToStudent).filter(TeacherToStudent.teacher_id == self.id,
                                                              TeacherToStudent.student_id == student.id).first()
            session.delete(relation)
            session.commit()
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
            if i not in ['surname', 'name', 'email']:
                return 2
            setattr(self, i, kwargs[i])
        return 0

    def user_type(self):
        return Teacher

    def invite(self, student_id):
        session = db_session.create_session()
        invites = session.query(TeacherInvite).filter(TeacherInvite.teacher_id == self.id).all()
        for i in invites:
            if i.student_id == student_id:
                return
        invite_ = TeacherInvite()
        invite_.teacher_id = self.id
        invite_.student_id = student_id
        session.add(invite_)
        session.commit()
