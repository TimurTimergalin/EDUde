from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.student import Student


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('password', required=True)
parser.add_argument('email', required=True)


def abort_if_teacher_not_found(student_id):
    session = db_session.create_session()
    student = session.query(Student).get(student_id)
    if not student:
        abort(404, message=f"News {student_id} not found")
        return
    return student


class TeacherResource(Resource):
    def get(self, student_id):
        teacher = abort_if_teacher_not_found(student_id)
        return jsonify({'teacher': teacher.to_dict(only=('surname', 'name'))})

    def delete(self, student_id):
        session = db_session.create_session()
        student = abort_if_teacher_not_found(student_id)
        session.delete(student)
        session.commit()
        return jsonify({'success': 'OK'})


class TeacherListResource(Resource):
    def get(self):
        session = db_session.create_session()
        student = session.query(Student).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in student]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        student = Student()
        student.surname = args['surname']
        student.name = args['name']
        student.email = args['email']
        student.set_password(args['password'])
        session.add(student)
        session.commit()
        return jsonify({'success': 'OK'})

