from distutils.ccompiler import show_compilers
from multiprocessing.sharedctypes import Value
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math
from flask import flash
import pprint
from flask_app.models.user import User

class Event:
    db = "mom_project"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.age = data['age']
        self.contact= data['contact']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data ['user_id']


    @classmethod 
    def get_all(cls):
        query =f"SELECT events.*, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at FROM events LEFT JOIN users ON events.user_id= users.id"
        results = connectToMySQL(cls.db).query_db(query)
        events = []
        for row in results:
            event = cls(row)
            user = {
            "id": row['user_id'],
            "first_name" : row['first_name'],
            "last_name" : row['last_name'],
            "email" : row['email'],
            "password" : row['password'],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at'],
        }
            event.user = User(user)
            events.append(event)
        return events

    @classmethod
    def update (cls, data):
        query = "UPDATE events SET name=%(name)s, location=%(location)s, age=%(age)s, contact=%(contact)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)


    @classmethod
    def get_one(cls,data):
        query ="SELECT * FROM events WHERE id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls (results[0])


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM events WHERE events.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def save(cls,data):
        query ="INSERT INTO events (name, location, age, contact, description,user_id) VALUES (%(name)s,%(location)s,%(age)s,%(contact)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_event_with_contact(cls,id):
        query =f"SELECT events.*, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at FROM events LEFT JOIN users ON events.user_id= users.id WHERE events.id= {id}"
        results = connectToMySQL(cls.db).query_db(query)
        event_with_contact = cls(results[0])

        user = {
            "id": results[0]['user_id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['created_at'],
            "updated_at" : results[0]['updated_at'],
        }
        event_with_contact.user = User (user)
        return event_with_contact
    
    @staticmethod
    def validate_event(event):
        is_valid = True
        if len(event['name']) <0:
            is_valid = False
            flash ("Must have name","event")
        if len(event['location']) <1:
            is_valid = False
            flash ("Please enter valid location", "event")
        if len(event['age']) <1:
            is_valid = False
            flash ("Please enter age range", "event")
        if len(event['contact']) <0:
            is_valid = False
            flash ("Please enter contact information", "event")
        if len(event['description']) <1:
            is_valid = False
            flash ("All Feilds Required","event")
        return is_valid


