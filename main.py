import sys
sys.path.insert(1, '/data')
from flask import Flask, render_template
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/start')
def start():
    return render_template('main_page.html')



# def main():
#     db_session.global_init("db/edu.sqlite")
#     session = db_session.create_session()
#     app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')