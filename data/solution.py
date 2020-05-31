import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from data.student_invite import StudentInvite
from data import db_session


class Solutions(SqlAlchemyBase):
    """Solution
    SQLAlchemy model of solutions"""
    __tablename__ = 'solutions'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    task_id = Cl(sql.Integer, sql.ForeignKey('tasks.id'))
    task = orm.relation('Task')
    student_id = Cl(sql.Integer, sql.ForeignKey('students.id'))
    student = orm.relation('Student')
    solution_link = Cl(sql.String)
