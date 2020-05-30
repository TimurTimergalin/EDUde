import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class FormTask(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'form_tasks'

    id = Cl(sql.Integer, autoincrement=True, primary_key=True)
    link = Cl(sql.String(128))


