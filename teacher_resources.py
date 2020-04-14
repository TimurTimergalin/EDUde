from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.teacher import Teacher
from create_user import create_user
from api_func import *


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('password', required=True)
parser.add_argument('email', required=True)

edit_parser = reqparse.RequestParser()
parser.add_argument('surname')
parser.add_argument('name')
parser.add_argument('email')


class TeacherResource(Resource):
    def get(self, teacher_id):
        teacher = abort_if_teacher_not_found(teacher_id)
        return jsonify({'teacher': teacher.to_dict(only=('surname', 'name'))})

    def put(self, teacher_id, teacher_password):
        teacher = abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        args = edit_parser.parse_args()
        for i in args:
            setattr(teacher, i, args[i])
        return jsonify({'success', 'OK'})

    def delete(self, teacher_id, teacher_password):
        session = db_session.create_session()
        teacher = abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        session.delete(teacher)
        session.commit()
        return jsonify({'success': 'OK'})


class TeacherListResource(Resource):
    def get(self):
        session = db_session.create_session()
        teacher = session.query(Teacher).all()
        return jsonify({'teachers': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in teacher]})

    def post(self):
        args = parser.parse_args()
        args['user_type'] = 'учитель'
        create_user(**args)
        return jsonify({'success': 'OK'})

