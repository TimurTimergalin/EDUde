import sys
sys.path.insert(1, '/data')
from flask import Flask, render_template
from data import db_session
from flask_restful import Api
import student_resources
import teacher_resources
import classroom_resources


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(student_resources.StudentResource, '/api/1.0/students/<int:id>')
api.add_resource(student_resources.StudentListResource, 'api/1.0/students')
api.add_resource(teacher_resources.TeacherResource, '/api/1.0/teacher/<int:id>')
api.add_resource(teacher_resources.TeacherListResource, '/api/1.0/teacher')
api.add_resource(classroom_resources.ClassRoomResource,
                 '/api/1.0/classroom/<int:teacher_id>/<int:teacher_password>/<int:class_room_id>')
api.add_resource(classroom_resources.ClassRoomListResource,
                 '/api/1.0/classroom/<int:teacher_id>/<int:teacher_password>')


@app.route('/start')
def start():
    return render_template('main_page.html')


@app.route('/start')
def start():
    return render_template('main_page.html')



# def main():
#     db_session.global_init("db/edu.sqlite")
#     session = db_session.create_session()
#     app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
