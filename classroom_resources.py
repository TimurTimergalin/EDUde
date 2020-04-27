from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.class_room import ClassRoom
from data.teacher import Teacher
from api_func import *


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('name')


class ClassRoomResource(Resource):
    def get(self, teacher_id, teacher_password, class_room_id):
        class_room = abort_if_class_not_found(class_room_id)
        abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        abort_if_request_is_forbidden(teacher_id, class_room_id)
        return jsonify({'classroom': class_room.to_dict(only=('id', 'name'))})

    def put(self, teacher_id, teacher_password, class_room_id):
        abort_if_teacher_not_found(teacher_id)
        abort_if_class_not_found(class_room_id)
        session = db_session.create_session()
        class_room = session.query(ClassRoom).get(class_room_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        abort_if_request_is_forbidden(teacher_id, class_room_id)
        args = edit_parser.parse_args()
        if args['name']:
            class_room.name = args['name']
        session.commit()
        return jsonify({'success': args})

    def delete(self, teacher_id, teacher_password, class_room_id):
        abort_if_class_not_found(class_room_id)
        abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        abort_if_request_is_forbidden(teacher_id, class_room_id)
        session = db_session.create_session()
        class_room = session.query(ClassRoom).get(class_room_id)
        session.delete(class_room)
        session.commit()
        return jsonify({'success': 'OK'})


class ClassRoomListResource(Resource):
    def get(self, teacher_id, teacher_password):
        session = db_session.create_session()
        abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        class_rooms = session.query(ClassRoom).filter(ClassRoom.teacher_id == teacher_id).all()
        return jsonify({'classrooms': [item.to_dict(only=('id', 'name')) for item in class_rooms]})

    def post(self, teacher_id, teacher_password):
        session = db_session.create_session()
        args = parser.parse_args()
        abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        class_room = ClassRoom()
        class_room.name = args['name']
        teacher = session.query(Teacher).get(teacher_id)
        teacher.add_class(class_room)
        session.add(class_room)
        session.commit()
        return jsonify({'success': args})
