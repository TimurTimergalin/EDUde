import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class StudentToClass(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'student_to_class'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    student_id = Cl(sql.Integer, sql.ForeignKey('students.id'))
    student = orm.relation('Student')
    classroom_id = Cl(sql.Integer, sql.ForeignKey('class_rooms.id'))
    classroom = orm.relation('ClassRoom')
