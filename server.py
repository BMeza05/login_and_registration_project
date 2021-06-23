from flask import Flask, render_template, redirect, request, session
# from werkzeug import datastructures
from flask_bcrypt import Bcrypt

from models.user import User


app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = "bruh"








@app.route('/')
def index():

    return render_template("index.html")


@app.route('/login', methods = ["POST"])
def login():
    if not User.login_validator(request.form):
        return redirect('/')
    
    user = User.get_by_email({"email": request.form['email']})

    session['uuid'] = user.id

    return redirect('/success')


@app.route('/register', methods = ["POST"])
def register():
    if not User.register_validator(request.form):
        return redirect('/')

    bruh = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bruh
    }

    user_id = User.create(data)

    session['uuid'] = user_id

    return redirect('/success')


@app.route('/success')
def success():
    return render_template("success.html")



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

