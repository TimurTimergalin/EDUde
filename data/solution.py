import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase


class Solution(SqlAlchemyBase):
    """Solution
    SQLAlchemy model of solutions"""
    __tablename__ = 'solutions'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    task_id = Cl(sql.Integer, sql.ForeignKey('tasks.id'))
    task = orm.relation('Task')
    student_id = Cl(sql.Integer, sql.ForeignKey('students.id'))
    student = orm.relation('Student')
    solution_link = Cl(sql.String)
    is_active = Cl(sql.Boolean, default=True)
    teachers_comment = Cl(sql.String(100))
