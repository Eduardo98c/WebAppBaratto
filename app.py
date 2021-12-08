from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home_app():
    print("ciao")
    return render_template('HomeTemplate.html')


@app.route('/LoginTemplate.html')
def login():
    return render_template('LoginTemplate.html')


@app.route('/RegistrationTemplate.html')
def registration():
    return render_template('RegistrationTemplate.html')


if __name__ == '__main__':
    app.run()
