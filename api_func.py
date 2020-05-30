from flask_restful import abort
from data import db_session
from data.teacher import Teacher
from data.class_room import ClassRoom
from data.student import Student
from data.normaltask import NormalTask
from generate_key import generate_key


def abort_if_class_not_found(class_room_id):
    session = db_session.create_session()
    class_room = session.query(ClassRoom).get(class_room_id)
    if not class_room:
        abort(404, message=f"Class {class_room_id} not found")
        return
    return class_room


def abort_if_teacher_not_found(teacher_id):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    if not teacher:
        abort(404, message=f"Teacher {teacher_id} not found")
        return
    return teacher


def abort_if_password_is_wrong(teacher_id, password):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    if not (generate_key(teacher) == password):
        abort(403, message="Wrong password")


def abort_if_password_is_wrong1(student_id, student_password):
    session = db_session.create_session()
    student = session.query(Student).get(student_id)
    if not (generate_key(student) == student_password):
        abort(403, message="Wrong password")


def abort_if_request_is_forbidden(teacher_id, class_room_id):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    class_room = session.query(ClassRoom).get(class_room_id)
    if class_room.teacher_id != teacher.id:
        abort(403, message=f"You are not allowed to get information about classroom #{class_room_id}")


def abort_if_student_not_found(student_id):
    session = db_session.create_session()
    student = session.query(Student).get(student_id)
    if not student:
        abort(404, message=f"Student {student_id} not found")
        return True
    return student


def abort_if_request_is_forbidden1(teacher_id, task_id):
    session = db_session.create_session()
    teacher = session.query(Teacher).get(teacher_id)
    task = session.query(NormalTask).get(task_id)
    for i in teacher.class_rooms:
        if task in i.tasks:
            return True
    abort(403, message="You are not allowed to get info about this task")


def abort_if_task_not_found(task_id):
    session = db_session.create_session()
    task = session.query(NormalTask).get(task_id)
    if not task:
        abort(404, message=f"Task {task_id} not found")
        return True
    return task


#  student in classroom of the task check
def abort_if_request_is_forbidden2(student_id, task_id):
    session = db_session.create_session()
    task = session.query(NormalTask).get(task_id)
    classroom = session.query(ClassRoom).get(task.class_room_id)
    student = session.query(Student).get(student_id)
    if student not in classroom.students:
        abort(403, message="You are not allowed to get info about this task")
