from crypt import methods
from flask_app import app
from flask import render_template, session, request, redirect
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

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

@app.route('/login')
def login_user():
    pass
