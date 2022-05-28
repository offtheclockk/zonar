from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app import DATABASE_SCHEMA
import re

class Event:
          def __init__( self , data ):
                    self.id = data['id']
                    self.D = data['D']
                    self.D1 = data['D1']
                    self.W = data['W']
                    self.W1 = data['W1']
                    self.OFF = data['OFF']
                    self.OFF1 = data['OFF1']
                    self.user_id = data['user_id']
                    self.created_at = data['created_at']
                    self.updated_at = data['updated_at']


          @classmethod
          def create_event(cls, data):
                    query = "INSERT INTO events (D, D1, W, W1, OFF, OFF1, user_id) VALUES (%(D)s, %(D1)s, %(W)s, %(W1)s, %(OFF)s, %(OFF1)s, %(user_id)s)"
                    return connectToMySQL(DATABASE_SCHEMA).query_db( query, data )

          @classmethod
          def get_all_events(cls):
                    query = "SELECT * FROM events"
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
                    if results:
                              all_events = []
                              for events in results:
                                        all_events.append(cls(events))
                              return all_events

          @classmethod
          def get_user_events(cls):
                    query = "SELECT * FROM events WHERE user_id = user_id;"
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query)
                    if results:
                              all_events = []
                              for events in results:
                                        all_events.append(cls(events))
                              return all_events

          @classmethod
          def get_one_event(cls, **data):
                    query = 'SELECT * FROM users LEFT JOIN events ON users.id = events.user_id WHERE users.id = user_id;'
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
                    if results:
                              return cls(results[0])
                    return results

          @classmethod
          def get_event_content(cls, **data):
                    query = 'SELECT * FROM events WHERE id = %(id)s;'
                    results = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
                    if results:
                              return cls(results[0])
                    return results

          @classmethod
          def update_one_event(cls, data):
                    query = 'UPDATE events SET D = %(D)s, D1 = %(D1)s, W = %(W)s, W1 = %(W1)s, OFF = %(OFF)s, OFF1 = %(OFF1)s WHERE id = %(id)s;'
                    return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

          @classmethod
          def delete_one_event(cls, data):
                    query = 'DELETE FROM events WHERE id = %(id)s;'
                    return connectToMySQL(DATABASE_SCHEMA).query_db(query, data)

          @staticmethod
          def validate_event(data):
                    is_valid = True

                    if len(data['D']) < 1:
                              is_valid = False
                              flash('Hours must be entered', "error_D")

                    if len(data['D1']) < 1:
                              is_valid = False
                              flash('Minutes must be entered', "error_D1")

                    if len(data['W']) < 1:
                              is_valid = False
                              flash('Minutes must be entered', "error_W")

                    if len(data['W1']) < 1:
                              is_valid = False
                              flash('Minutes must be entered', "error_W1")

                    if len(data['OFF']) < 1:
                              is_valid = False
                              flash('Minutes must be entered', "error_OFF")

                    if len(data['OFF1']) < 1:
                              is_valid = False
                              flash('Minutes must be entered', "error_OFF1")

                    return is_valid