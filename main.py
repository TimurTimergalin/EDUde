import sys
sys.path.insert(1, '/data')
from flask import Flask
from data import db_session
from data.teacher import Teacher


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/edu.sqlite")
    session = db_session.create_session()
    teacher = Teacher(surname='dpgjrg',
                      name='rgjhrg')
    print(dir(teacher.students))
    app.run()


if __name__ == '__main__':
    main()