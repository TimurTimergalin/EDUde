from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.student import Student
from create_user import create_user
from api_func import *

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('surname')
edit_parser.add_argument('name')
edit_parser.add_argument('email')


class StudentResource(Resource):
    def put(self, student_id, student_password):
        print(student_id, student_password)
        session = db_session.create_session()
        student = session.query(Student).get(student_id)
        abort_if_student_not_found(student_id)
        abort_if_password_is_wrong1(student_id, student_password)
        args = edit_parser.parse_args()
        for i in args:
            if not args[i]:
                continue
            setattr(student, i, args[i])
        session.commit()
        return jsonify({'success': args})

    def delete(self, student_id, student_password):
        session = db_session.create_session()
        student = session.query(Student).get(student_id)
        abort_if_student_not_found(student_id)
        abort_if_password_is_wrong1(student_id, student_password)
        session.delete(student)
        session.commit()
        return jsonify({'success': 'OK'})


class StudentListResource(Resource):
    def get(self, teacher_id):
        session = db_session.create_session()
        abort_if_teacher_not_found(teacher_id)
        teacher = session.query(Teacher).get(teacher_id)
        student = session.query(Student).filter(teacher in Student.teachers).all()
        return jsonify({'students': [item.to_dict(
            only=('id', 'name', 'surname')) for item in student]})


class StudentGetResource(Resource):
    def get(self, student_id):
        teacher = abort_if_student_not_found(student_id)
        return jsonify({'student': teacher.to_dict(only=('id', 'surname', 'name'))})


