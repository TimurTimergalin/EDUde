from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.class_room import ClassRoom
from data.teacher import Teacher
from data.task import Task
from api_func import *


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('deadline')
parser.add_argument('link')


class TaskResource(Resource):
    def get(self, teacher_id, teacher_password, task_id):
        task = abort_if_task_not_found(task_id)
        abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        abort_if_request_is_forbidden1(teacher_id, task_id)
        return jsonify({'task': task.to_dict(only=('id', 'name'))})

    def delete(self, teacher_id, teacher_password, task_id):
        task = abort_if_task_not_found(task_id)
        abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        abort_if_request_is_forbidden1(teacher_id, task_id)
        session = db_session.create_session()
        session.delete(task)
        return jsonify({'success': 'OK'})


class TaskListResource(Resource):
    def get(self, teacher_id, teacher_password):
        teacher = abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        return jsonify({'tasks': [{class_room.name: [item.to_dict(only=('id', 'name')) for item in class_room.tasks]}
                                  for class_room in teacher.class_rooms]})

    def post(self, teacher_id, teacher_password):
        session = db_session.create_session()
        args = parser.parse_args()
        abort_if_teacher_not_found(teacher_id)
        abort_if_password_is_wrong(teacher_id, teacher_password)
        task = Task()
        task.name = args['name']
        task.deadline = args['deadline']
        task.link = args['link']
        session.add(task)
        session.commit()
        return jsonify({'success': 'OK'})