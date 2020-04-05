from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.class_room import ClassRoom
from data.teacher import Teacher


parser = reqparse.RequestParser()
parser.add_argument('name')


def abort_if_class_not_found(class_room_id):
    session = db_session.create_session()
    class_room = session.query(ClassRoom).get(class_room_id)
    if not class_room:
        abort(404, message=f"News {class_room_id} not found")
        return
    return class_room


def abort_if_password_is_wrong(teacher_id, password):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    if not teacher.check_password(password):
        abort(402, message="Wrong password")


def abort_if_request_is_forbidden(teacher_id, class_room_id):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    class_room = session.query(ClassRoom).get(class_room_id)
    if class_room.teacher_id != teacher.id:
        abort(403, message=f"You are not allowed to get information about classroom #{class_room_id}")


class ClassRoomResource(Resource):
    def get(self, teacher_id, teacher_password, class_room_id):
        class_room = abort_if_class_not_found(class_room_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        abort_if_request_is_forbidden(teacher_id, class_room_id)
        return jsonify({'classroom': class_room.to_dict(only=('id', 'name'))})

    def delete(self, teacher_id, teacher_password, class_room_id):
        class_room = abort_if_class_not_found(class_room_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        abort_if_request_is_forbidden(teacher_id, class_room_id)
        session = db_session.create_session()
        session.delete(class_room)
        session.commit()
        return jsonify({'success': 'OK'})


class ClassRoomListResource(Resource):
    def get(self, teacher_id, teacher_password):
        session = db_session.create_session()
        abort_if_password_is_wrong(teacher_id, teacher_password)
        class_rooms = session.query(ClassRoom).filter(ClassRoom.teacher_id == teacher_id).all()
        return jsonify({'classrooms': [item.to_dict(only=('id', 'name')) for item in class_rooms]})

    def post(self, teacher_id, teacher_password):
        session = db_session.create_session()
        args = parser.parse_args()
        abort_if_password_is_wrong(teacher_id, teacher_password)
        class_room = ClassRoom()
        class_room.name = args['name']
        teacher = session.query(Teacher).get(teacher_id)
        teacher.add_class(class_room)
        session.add(class_room)
        session.commit()
        return jsonify({'success': 'OK'})
