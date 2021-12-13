from flask import Flask, render_template

from Database.databaseAlchemy import db_session, init_db
from Database.users_db import form_user

app = Flask(__name__)
db = init_db()


@app.route('/')
def home_app():
    return render_template('index.html')


@app.route('/index.html')
def return_to_home():
    return render_template('index.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/registrazione.html', methods=['GET', 'POST'])
def registration():
    form_user(db)
    return render_template('registrazione.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
