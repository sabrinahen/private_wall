from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import message
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "private_wall_schema"
    def __init__ (self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VAlUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getEmail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getId(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
            is_valid = True
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(User.db).query_db(query,user)
            if len(results) >= 1:
                flash("Email already taken. Try again!")
                is_valid=False
            if not EMAIL_REGEX.match(user['email']):
                flash("Invalid Email. Try again!")
                is_valid=False
            if len(user['first_name']) < 2:
                flash("First name must be at least 2 characters")
                is_valid= False
            if len(user['last_name']) < 2:
                flash("Last name must be at least 2 characters")
                is_valid= False
            if len(user['password']) < 8:
                flash("Password must be at least 8 characters")
                is_valid= False
            if user['confirm'] != user['password']:
                flash("Passwords don't match. Try again!")
            return is_valid