from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.dashboard import Event

class Comment:
    db = "mom_project"
    def __init__(self,data):
        self.id = data['id']
        self.details = data['details']
        self.user_id= data['user_id']
        self.event_id= data['event_id']

    @classmethod 
    def get_comments_for_event(cls,event_id):
        query = " SELECT comments.*, events.name, events.location, events.age, events.contact, events.description, events.created_at, events.updated_at FROM comments LEFT JOIN events ON comments.event_id= events.id WHERE events.id = %(event_id)s;"
        data= {
            "event_id": event_id
        }
        results = connectToMySQL(cls.db).query_db(query,data)
        comments = []
        for row in results:
            comment = cls(row)
            event = {
            "id": row['event_id'],
            "name" : row['name'],
            "location" : row['location'],
            "age" : row['age'],
            "contact" : row['contact'],
            "description" : row['description'],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at'],
            "user_id" : row['user_id'],
        }
            comment.event = Event(event)
            comments.append(comment)
        return comments

    @classmethod
    def save(cls,data):
        query ="INSERT INTO comments (details, user_id, event_id) VALUES (%(details)s,%(user_id)s,%(event_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['details']) >3:
            is_valid = False
            flash ("Must have 3 characters","comment")
        return is_valid