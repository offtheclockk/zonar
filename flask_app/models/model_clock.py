from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app import DATABASE_SCHEMA
import re
from flask_bcrypt import Bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Clock:
          def __init__( self , data ):
                    self.id = data['id']
                    self.drive_clock = data['drive_clock']
                    self.work_clock = data['work_clock']
                    self.off_clock = data['off_clock']
                    self.violation_status = data['violation_status']
                    self.time_value = data['time_value']
                    self.created_at = data['created_at']
                    self.updated_at = data['updated_at']


          @classmethod
          def create_clock(cls, data):
                    query = "INSERT INTO clocks (drive_clock, work_clock, off_clock, violation_status, time_value, user_id) VALUES (%(drive_clock)s, %(work_clock)s, %(off_clock)s, %(violation_status)s, %(time_value)s, %(user_id)s)"
                    return connectToMySQL(DATABASE_SCHEMA).query_db( query, data )

          @classmethod
          def add_value(cls, data):
                    query = "SELECT SUM(drive_value + work_value) FROM clocks WHERE user_id = user_id;"
                    return connectToMySQL(DATABASE_SCHEMA).query_db( query, data)

          @classmethod
          def get_all_clocks(cls):
                    query = "SELECT * FROM clocks;"
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
                    if results:
                              all_clocks = []
                              for clocks in results:
                                        all_clocks.append(cls(clocks))
                              return all_clocks

          @classmethod
          def get_user_clocks(cls):
                    query = "SELECT * FROM clocks WHERE user_id = user_id;"
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
                    if results:
                              all_clocks = []
                              for clocks in results:
                                        all_clocks.append(cls(clocks))
                              return all_clocks

          @classmethod
          def get_one_name(cls, **data):
                    query = 'SELECT * FROM users LEFT JOIN clocks ON users.id = clocks.user_id WHERE users.id = user_id;'
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
                    if results:
                              return cls(results[0])
                    return results

          @classmethod
          def get_content(cls, **data):
                    query = 'SELECT * FROM clocks WHERE id = %(id)s;'
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
                    if results:
                              return cls(results[0])
                    return results

          @classmethod
          def update_one(cls, data):
                    query = 'UPDATE clocks SET type = %(type)s, violation_status = %(violation_status)s, time_value = %(time_value)s, WHERE id = %(id)s;'
                    return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

          @classmethod
          def delete_one(cls, data):
                    query = 'DELETE FROM clocks WHERE id = %(id)s;'
                    return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

          @staticmethod
          def validate_clock(data):
                    is_valid = True

                    if len(data['drive_clock']) < 1:
                              is_valid = False
                              flash('Type of clock must be selected', "error_type")

                    if len(data['work_clock']) < 1:
                              is_valid = False
                              flash('Type of clock must be selected', "error_type")

                    if len(data['off_clock']) < 1:
                              is_valid = False
                              flash('Type of clock must be selected', "error_type")

                    if len(data['violation_status']) < 2:
                              is_valid = False
                              flash('Genre must be greater than 2 characters', "error_genre")

                    if len(data['time_value']) < 2:
                              is_valid = False
                              flash('Time Value must be greater than 2 characters', "error_city")

                    return is_valid