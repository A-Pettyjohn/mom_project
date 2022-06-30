from crypt import methods
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.dashboard import Event
from flask_app.models.like import Like
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/register', methods=['POST'])
def register():
    is_valid = User.validate_register(request.form)

    if not is_valid:
        return redirect('/')

    new_user ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    id = User.save(new_user)
    print("USER SAVED!!!")
    session['user_id'] = id
    return redirect ('/')


@app.route('/login', methods=["POST"])
def login():
    print("login was called!!!!!!!!!!!!!!!!!!!!")
    data = {
        "email": request.form['email']
    }
    print (f"DATA IS : {data}")
    user = User.get_by_email(data)
    print("*********************")
    print(user.password)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    # data = {
    #     'id': session['user_id']
    # }
    user_data = {
            "id" : session ['user_id']
        }
    user_id = session['user_id']
    return render_template('dashboard.html', events=Event.get_all(), likes=Like.rsvp(user_id) ,user=User.get_by_id(user_data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


