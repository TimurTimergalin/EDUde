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
    name = Cl(sql.String(32))
    description = Cl(sql.Text)
    deadline = Cl(sql.DateTime)
    link = Cl(sql.String(128))
    class_room_id = Cl(sql.Integer, sql.ForeignKey('class_rooms.id'))
    class_room = orm.relation('ClassRoom')
    solutions = orm.relation('Solution', back_populates='task')
    form_link = Cl(sql.String(128))
    status = Cl(sql.Boolean, default=1)

    def __repr__(self):
        return f'Task#{self.id}: {self.name}'

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

    def is_google(self):
        if type(self.form_link) == str:
            return True
        return False
