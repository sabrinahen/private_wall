from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.message import Message

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    print(request.form["email"])
    user = User.getEmail(request.form)
    if not user:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.getId(data)
    messages = Message.get_user_messages(data)
    users = User.getAll()
    return render_template("dashboard.html",user=user,users=users,messages=messages)

@app.route('/logout')
def logout():
    session.clear()
    flash("You are logged out!")
    return redirect('/')