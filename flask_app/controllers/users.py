from flask import render_template,redirect,session,request, flash
from flask_app import app
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
    user = User.get_with_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')
    # data ={
    #     "email" : request.form["email"]
    # }
    # user_db =  User.get_with_email(data) #returns User cls
    # print(user_db)
    # if not user_db:
    #     flash("Invalid email/password", "login")
    #     return redirect('/')
    # if not bcrypt.check_password_hash(user_db.password, request.form["password"]):
    #     flash("Invalid email/password", "login")
    #     return redirect('/')
    # session ={ "userid" : request.form['user.id'],
    # "first_name": request.form["first_name"],
    # "login": True}
    # return redirect("/dashboard")

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash('You need to log into account','login')
        return redirect('/')
    return render_template("dashboard.html", user=session)