import sys
sys.path.insert(1, '/data')
from flask import Flask
from data import db_session
from flask_restful import Api
import student_resources
import teacher_resources


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(student_resources.StudentResource, '/api/1.0/students/<int:id>')
api.add_resource(student_resources.StudentListResource, 'api/1.0/students')
api.add_resource(teacher_resources.TeacherResource, '/api/1.0/teacher/<int:id>')
api.add_resource(teacher_resources.TeacherListResource, 'api/1.0/teacher')


def main():
    db_session.global_init("db/edu.sqlite")
    session = db_session.create_session()
    app.run()


if __name__ == '__main__':
    main()