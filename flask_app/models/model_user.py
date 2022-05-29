from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app import DATABASE_SCHEMA
import re
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
          def __init__( self , data ):
                    self.id = data['id']
                    self.first_name = data['first_name']
                    self.last_name = data['last_name']
                    self.email = data['email']
                    self.hash_pw = data['hash_pw']
                    self.created_at = data['created_at']
                    self.updated_at = data['updated_at']


          @classmethod
          def create(cls, data):
                    query = "INSERT INTO users (first_name, last_name, email, hash_pw) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(hash_pw)s);"
                    return connectToMySQL(DATABASE_SCHEMA).query_db( query, data )

          @classmethod
          def get_all(cls):
                    query = "SELECT * FROM users;"
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
                    if results:
                              all_users = []
                              for users in results:
                                        all_users.append(cls(users))
                    return all_users

          @classmethod
          def get_one_email(cls, **data):
                    query = 'SELECT * FROM users WHERE email = %(email)s;'
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
                    if results:
                              return cls(results[0])
                    return results

          @classmethod
          def get_one(cls, data):
                    query = 'SELECT * FROM users WHERE users.id = %(id)s;'
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
                    if results:
                              return cls(results[0])
                    return results

          @classmethod
          def update_one(cls, data):
                    query = 'UPDATE users SET first_name = %(first_name)s WHERE id=%(id)s;'
                    return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

          @classmethod
          def delete_one(cls, data):
                    query = 'DELETE FROM users WHERE id=%(id)s;'
                    connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
                    return id

          @staticmethod
          def validate_user(data):
                    is_valid = True

                    if len(data['first_name']) < 1:
                              is_valid = False
                              flash('First name must be greater than 1 character', "error_first_name")

                    if len(data['last_name']) < 1:
                              is_valid = False
                              flash('Last name must be greater than 1 character', "error_last_name")

                    if len(data['email']) < 2:
                              is_valid = False
                              flash('Email must be greater than 2 characters', "error_email")
                    elif not EMAIL_REGEX.match(data['email']):
                              flash("Invalid email address")
                              is_valid = False

                    if len(data['pw']) < 8:
                              is_valid = False
                              flash('Password must be greater than 8 characters', "error_pw")

                    if (data['confirm_pw'] != data['pw']):
                              is_valid = False
                              flash('Passwords must match', "error_confirm_pw")

                    return is_valid