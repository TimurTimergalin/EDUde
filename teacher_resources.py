from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.teacher import Teacher
from create_user import create_user
from api_func import *

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('surname')
edit_parser.add_argument('name')
edit_parser.add_argument('email')


class TeacherResource(Resource):
    def put(self, teacher_id, teacher_password):
        abort_if_teacher_not_found(teacher_id)
        session = db_session.create_session()
        teacher = session.query(Teacher).get(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        args = edit_parser.parse_args()
        for i in args:
            if not args[i]:
                continue
            setattr(teacher, i, args[i])
        session.commit()
        return jsonify({'success': args})

    def delete(self, teacher_id, teacher_password):
        session = db_session.create_session()
        abort_if_teacher_not_found(teacher_id)
        teacher = session.query(Teacher).get(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        session.delete(teacher)
        session.commit()
        return jsonify({'success': 'OK'})


class TeacherGetResource(Resource):
    def get(self, teacher_id):
        teacher = abort_if_teacher_not_found(teacher_id)
        return jsonify({'teacher': teacher.to_dict(only=('id', 'surname', 'name'))})


class TeacherListResource(Resource):
    def get(self):
        session = db_session.create_session()
        teacher = session.query(Teacher).all()
        return jsonify({'teachers': [item.to_dict(
            only=('id', 'name', 'surname')) for item in teacher]})


