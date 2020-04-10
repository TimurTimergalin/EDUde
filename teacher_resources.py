from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.teacher import Teacher
from create_user import create_user


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('password', required=True)
parser.add_argument('email', required=True)


def abort_if_teacher_not_found(teacher_id):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    if not teacher:
        abort(404, message=f"News {teacher_id} not found")
        return
    return teacher


class TeacherResource(Resource):
    def get(self, teacher_id):
        teacher = abort_if_teacher_not_found(teacher_id)
        return jsonify({'teacher': teacher.to_dict(only=('surname', 'name'))})

    def delete(self, teacher_id):
        session = db_session.create_session()
        teacher = abort_if_teacher_not_found(teacher_id)
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

