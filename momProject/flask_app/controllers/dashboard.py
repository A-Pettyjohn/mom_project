from crypt import methods
from pprint import pprint

from flask import render_template, session, flash, redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.dashboard import Event
from flask_app.models.comment import Comment
from flask_app.models.like import Like


@app.route('/new')
def create():
    if 'user_id' not in session:
        return redirect ('/logout')

    data = {
        "id":session['user_id']
    }
    return render_template ('create.html',user=User.get_by_id(data))

@app.route('/new/event',methods=['POST'])
def add_event():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/new')
    data = {
        "name": request.form["name"],
        "location": request.form["location"],
        "age": request.form["age"],
        "contact": request.form["contact"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Event.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_event(id):
    if'user_id' not in session:
        return redirect ('/logout')
    data = {
        "id":id
    }
    user_data= {
        "id":session['user_id']
    }
    return render_template("edit.html", edit=Event.get_one(data),user =User.get_by_id(user_data))

@app.route('/update/event', methods=['POST'])
def update_event():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/dashboard')
    data = {
        "name": request.form["name"],
        "location": request.form["location"],
        "age": request.form["age"],
        "contact": request.form["contact"],
        "description": request.form["description"],
        "user_id": session["user_id"],
        "id": request.form["id"]
    }
    Event.update(data)
    return redirect('/dashboard')

@app.route('/show_event/<int:event_id>')
def show_event_with_contact(event_id):
    event = Event.get_event_with_contact(event_id)
    comments = Comment.get_comments_for_event(event_id)
    session['event_id'] = event_id
    return render_template ('show.html', event=event, comments=comments)


@app.route('/event/<int:id>')
def show_event (id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id" : id
    }
    user_data = {
        "id" : session ['user_id']
    }
    return render_template("show.html", event=Event.get_one(data), user=User.get_by_id(user_data))

@app.route('/destroy/event/<int:id>')
def destroy_event(id):
    data ={
        "id" : id
    }
    Event.destroy(data)
    return redirect('/dashboard')

# @app.route('/show_event/<int:id>')
# def add_comment():
#     if 'user_id' not in session:
#         return redirect ('/logout')
#     data ={
#         "id":session['user_id']
#     }
#     return render_template ('show.html',user=User.get_by_id(data))

@app.route('/save_comment', methods=['POST'])
def save_comment():
    if 'user_id' not in session:
        return redirect('/logout')
    event_id=str(session["event_id"])
    redirect_url='/show_event/' + event_id
    print(request.form['details'])
    # if not Comment.validate_comment(request.form):
    #     return redirect (redirect_url)
    data = {
        "details": request.form["details"],
        "user_id": session["user_id"],
        "event_id": session["event_id"]
    }
    Comment.save(data)
    return redirect(redirect_url)

@app.route('/rsvp', methods=['GET'])
def rsvp():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session["user_id"],
        "event_id": session["event_id"],
    }
    Like.save(data)
    return redirect ('/dashboard')