from flask_app.config.mysqlconnection import MySQLConnection
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
Letter_pattern = re.compile("^[a-zA-Z]+$")

class User:
    db = "login_registration"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        query ="INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, Now(), Now()); "
        return MySQLConnection(cls.db).query_db(query,data)
        
    @classmethod
    def get_with_email(cls,data):
        query=" SELECT * FROM users where email = %(email)s"
        result = MySQLConnection(cls.db).query_db(query,data)
        print(result)
        if len(result) < 1:
            return False
        user = cls(result[0])
        return user

    @staticmethod
    def validate_reg(user):
        is_valid = True
        query="SELECT * FROM users WHERE email = %(email)s"
        result = MySQLConnection(User.db).query_db(query, user)
        if len(user["first_name"]) < 3 :
            flash("First name is to be longer than 3 characters", "reg")
            is_valid = False
        if not Letter_pattern.match(user["first_name"]):
            flash("First name can only contain letters", "reg")
            is_valid = False
        if len(user["last_name"]) < 3 :
            flash("Last name is to be longer than 3 characters", "reg")
            is_valid = False
        if not Letter_pattern.match(user["last_name"]):
            flash("Last name can only contain letters", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address", "reg")
            is_valid = False
        if len(result) >= 1:
            flash("Email already exists, Please use different email", "reg")
            is_valid = False
        if user["password"] != user["password_confirm"]:
            flash("Passwords do not match, Please type in matching password", "reg")
            is_valid = False
        if len(user["password"]) > 8:
            flash("password needs to be at least 8 characters long", "reg")
            is_valid = False
        return is_valid