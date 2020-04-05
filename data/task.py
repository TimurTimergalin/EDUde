import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Task(SqlAlchemyBase, SerializerMixin):
    """Task
    SQLAlchemy model of task"""
    __tablename__ = 'tasks'

    id = Cl(sql.Integer, autoincrement=True, primary_key=True)
    name = Cl(sql.String)
    description = Cl(sql.Text)
    deadline = Cl(sql.DateTime)
    link = Cl(sql.String)
    class_room_id = Cl(sql.Integer, sql.ForeignKey('class_rooms.id'))
    class_room = orm.relation('ClassRoom')

    def set_deadline(self, deadline):
        """Task.set_deadline
        Change a dealine of the task"""
        self.deadline = deadline
