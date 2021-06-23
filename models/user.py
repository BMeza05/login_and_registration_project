from flask import Flask
from config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)




class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL("users_login").query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])



    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE email = %(id)s;"

        results = connectToMySQL("users_login").query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])


    @classmethod
    def create(cls, data):
        query = "INSERT INTO users_login.users ( first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(),NOW());"

        user_id = connectToMySQL("users_login").query_db(query, data)

        return user_id

    @staticmethod
    def register_validator(post_data):
        is_valid= True

        if len(post_data['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False

        if len(post_data['last_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(post_data['email']):
            flash('not a valid email format')
            is_valid = False

        if len(post_data['password']) < 4:
            flash("Password must be at least 4 characters")
            is_valid = False
        else:
            if post_data['password'] != post_data['confirm_password']:
                flash('password must match')
            is_valid = False

        return is_valid

    @staticmethod
    def login_validator(post_data):
        user_from_db = User.get_by_email({'email': post_data['email']})
        if not user_from_db:
            flash("invalid email")
            return False

        if not bcrypt.check_password_hash(user_from_db.password, post_data['password']):
            flash("invalid password")
            return False

        return True