from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home_app():
    return render_template('index.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/registrazione.html')
def registration():
    return render_template('registrazione.html')


if __name__ == '__main__':
    app.run()
