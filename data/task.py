import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'
    id = Cl(sql.Integer, autoincrement=True, primary_key=True)
    name = Cl(sql.String(32))
    normal_id = Cl(sql.Integer, sql.ForeignKey('normal_tasks.id'), nullable=True)
    form_id = Cl(sql.Integer, sql.ForeignKey('form_tasks.id'), nullable=True)
    classroom_id = Cl(sql.Integer, sql.ForeignKey('class_rooms.id'))
    classroom = orm.relation('ClassRoom')
    deadline = Cl(sql.DateTime)
    link = Cl(sql.String(128))
    status = Cl(sql.Boolean, default=1)





