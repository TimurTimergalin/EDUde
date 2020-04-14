from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.student import Student
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


class StudentResource(Resource):
    def get(self, student_id):
        teacher = abort_if_student_not_found(student_id)
        return jsonify({'student': teacher.to_dict(only=('surname', 'name'))})

    def put(self, student_id, student_password):
        student = abort_if_teacher_not_found(student_id)
        abort_if_password_is_wrong1(student_id, student_password)
        args = edit_parser.parse_args()
        for i in args:
            setattr(student, i, args[i])
        return jsonify({'success', 'OK'})

    def delete(self, student_id, student_password):
        session = db_session.create_session()
        student = abort_if_student_not_found(student_id)
        abort_if_password_is_wrong1(student_id, student_password)
        session.delete(student)
        session.commit()
        return jsonify({'success': 'OK'})


class StudentListResource(Resource):
    def get(self):
        session = db_session.create_session()
        student = session.query(Student).all()
        return jsonify({'students': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in student]})

    def post(self):
        args = parser.parse_args()
        args['user_type'] = 'ученик'
        create_user(**args)
        return jsonify({'success': 'OK'})

