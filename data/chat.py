import sys
sys.path.insert(1, '/data')
import sqlalchemy as sql
from sqlalchemy import Column as Cl
from data.db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase):
    """Chat
        SQLAlchemy model of chat"""
    __tablename__ = 'chats'

    chat_id = Cl(sql.Integer, autoincrement=True, primary_key=True)
    task_id = Cl(sql.Integer)
    teacher_id = Cl(sql.Integer)
    student_id = Cl(sql.Integer)


class Message(SqlAlchemyBase):
    """Message
        SQLAlchemy model of message"""
    __tablename__ = 'messages'

    message_id = Cl(sql.Integer, autoincrement=True, primary_key=True)
    chat_id = Cl(sql.Integer)
    user_id = Cl(sql.Integer)
    content = Cl(sql.String)
    # date_create = Cl(sql.DateTime)
    is_active = Cl(sql.Boolean, default=True)

    def delete_message(self, user_id):
        try:
            if user_id != self.user_id:
                return 1
            self.is_active = False
        except Exception:
            return 1

    def change_message(self, user_id, content):
        try:
            if user_id != self.user_id:
                return 1
            self.content = content
        except Exception:
            return 1
