import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class NormalTask(SqlAlchemyBase, SerializerMixin):
    """Task
    SQLAlchemy model of task"""
    __tablename__ = 'normal_tasks'

    id = Cl(sql.Integer, autoincrement=True, primary_key=True)
    description = Cl(sql.Text)

    def set_deadline(self, deadline):
        """Task.set_deadline
        Change a dealine of the task"""
        self.deadline = deadline

    def edit_myself(self, **kwargs):
        """ClassRoom.edit_myself
        edit the current object"""
        if not kwargs:
            return 1
        for i in kwargs:
            if i not in ['name', 'description', 'deadline', 'link']:
                return 2
            setattr(self, i, kwargs[i])
        return 0
