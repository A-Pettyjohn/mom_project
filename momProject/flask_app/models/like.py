from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.dashboard import Event
from flask_app.models.comment import Comment

class Like:
    db = "mom_project"
    def __init__(self,data):
        self.user_id = data['user_id']
        self.event_id= data['event_id']

    @classmethod
    def save(cls,data):
        query ="INSERT INTO users_has_events (user_id, event_id) VALUES (%(user_id)s,%(event_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def rsvp(cls,user_id):
        data ={
            "user_id": user_id
        }
        query ="SELECT users_has_events.*, events.* FROM users_has_events LEFT JOIN events ON users_has_events.event_id = events.id WHERE users_has_events.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        liked_events=[]
        for row in results:
            liked_event = {
                "id": row['event_id'],
                "name" : row['name'],
                "location" : row['location'],
                "age" : row['age'],
                "contact" : row['contact'],
                "description" : row['description'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : row['events.user_id'],
            }
            liked_events.append(Event(liked_event))
        return liked_events