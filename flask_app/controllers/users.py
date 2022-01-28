from crypt import methods
from flask_app import app
from flask import render_template, session, request, redirect, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    if not User.validate_reg(request.form):
        return redirect('/')
    pwd_h = bcrypt.generate_password_hash(request.form["password"])
    
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pwd_h
    }
    User.save(data)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login_user():
    data ={
        "email" : request.form["email"]
    }
    user_db =  User.get_with_email(data) #returns User cls
    if not user_db:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.password, request.form["password"]):
        flash("Invalid email/password", "login")
        return redirect('/')
    session ={ "userid" : request.form['user.id'],
    "first_name": request.form["first_name"],
    "login": True}
    return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if not session['login']:
        flash('You need to log into account','login')
        return redirect('/')
    return render_template("dashboard.html", user=session)
