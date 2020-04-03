import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = Cl(sql.Integer, primary_key=True, autoincrement=True)
    name = Cl(sql.String)

    def __repr__(self):
        return self.name
