import os
import random

from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from flask_session import Session
from datetime import datetime, date

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["SECRET_KEY"] = "some key"
socketio = SocketIO(app)

pro_photo = ["adil-zhanbyrbayev-PMfjeWpz0Tc-unsplash.jpg","clement-eastwood-Gtz39oChT0A-unsplash.jpg","gemma-chua-tran-qGRKrp7ITqw-unsplash.jpg","gemma-chua-tran-qGRKrp7ITqw-unsplash.jpg","gemma-chua-tran-qGRKrp7ITqw-unsplash.jpg","in-lieu-in-view-photography-6ZXoZALOBWE-unsplash.jpg", "isaac-owens-W55q-GkyrzA-unsplash.jpg", "johan-de-jager--olnD7LIpD0-unsplash.jpg", "johan-de-jager-Os7h_zifF0Y-unsplash.jpg", "johan-de-jager-Os7h_zifF0Y-unsplash.jpg", "johan-de-jager-Os7h_zifF0Y-unsplash.jpg"]
    
now = datetime.time(datetime.now())
time = now.strftime("%-I:%M %p") 
print(f"{time}")

@app.route("/", methods=["GET", "POST"])
def index():
        
    if session.get("users") is None:
        session["users"] = {}
    if session.get("channel_messages") is None:
        session["channel_messages"] = {}
        
        
    if request.method == "GET":
        if session.get("users") is None:
            return render_template("index.html")
        if session.get("user_name"): 
            if session.get("users"):
                username = session.get("user_name")
                channel_list = session["users"][username]["channel_list"]
                
                return render_template("profile.html", username=session["user_name"], user=session["users"][username], channel_list=channel_list)
        else: 
            return render_template("index.html")
        

    if request.method == "POST":
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        
        newuser = {username: {"username": username, "firstname": firstname, "lastname": lastname, "image": random.choice(pro_photo), "channel_list":['welcome']}}
        session["user_name"] = username
        session["users"].update(newuser)
        channel_list = session["users"][username]["channel_list"]
        
        
        
        return render_template("profile.html", username=session["user_name"], user=session["users"][username], channel_list=channel_list)
    return render_template("index.html")     

@app.route("/signin", methods=["GET", "POST"])
def signin():
    username = request.form.get("username")
    if session.get("users") is None:
        session["users"] = {}
    if session.get("channel_messages") is None:
        session["channel_messages"] = {}
        
    if request.method == "GET":
        if session.get("users") is None:
            return render_template("index.html")
        if session.get("user_name"): 
            if session.get("users"):
                username = session.get("user_name")
                channel_list = session["users"][username]["channel_list"]
                
                return render_template("profile.html", username=session["user_name"], user=session["users"][username], channel_list=channel_list)
        else: 
            return render_template("signin.html")
        

        if request.method == "POST":
            session["user_name"] = username
            channel_list = session["users"][username]["channel_list"]
            
            return render_template("profile.html", username=session["user_name"], user=session["users"][username], channel_list=channel_list)
    return render_template("signin.html")



@app.route("/profile", methods=["GET", "POST"])
def profile():
    if session.get("users") is None:
        session["users"] = {}
    if session.get("channel_messages") is None:
        session["channel_messages"] = {}
        
    if request.method == "GET":
        if session.get("users") is None:
            return render_template("index.html")
        if session.get("user_name"): 
            if session.get("users"):
                username = session.get("user_name")
                channel_list = session["users"][username]["channel_list"]
                user_info = session['users'][username]
                
                
                return render_template("profile.html", username=session["user_name"], user=session["users"][username], channel_list=channel_list), jsonify({"success": True, "chan_list": channel_list, "user_info": user_info})
        else: 
            return render_template("index.html")
        

        return render_template("profile.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    username = session.get('user_name')
    a_message = "Please choose a different channel name."
    channel_name = request.form.get('channel-name')
    if request.method == "GET":
        return render_template("create.html")
    
    if request.method == "POST" and channel_name not in session["users"][username]["channel_list"]:
        
        the_list = session["users"][username]["channel_list"]
        the_list.append(channel_name)
        new_message_list = {channel_name: []}
        session["channel_messages"].update(new_message_list)
        
            
        return redirect("/channel/" + channel_name)
    return render_template("create.html", a_message=a_message)

@socketio.on("send message")
@app.route("/channel/<channel_name>", methods=["GET", "POST"])
def channel(channel_name):
    username = session.get('user_name')
 

    if request.method == "GET":
        if session.get("user_name"):
            if channel_name == 'welcome':
                welcome = {'welcome': []}
                session["channel_messages"].update(welcome)
                welcome_msg = {"username": "flack", "date": time, "message": "Welcome to flack!", "image": "artur-tumasjan-IDbeTFgI9As-unsplash.jpg" }
                session["channel_messages"]['welcome'].append(welcome_msg)
                all_messages = session["channel_messages"][channel_name]
                session["channel_name"] = channel_name

                
            if session.get("users"):
                username = session.get('user_name')
                channel_list = session["users"][username]["channel_list"]
                all_messages = session["channel_messages"][channel_name]
                session["channel_name"] = channel_name

                
                return render_template("msgs.html", messages=all_messages, channel_name=channel_name, username=session["user_name"], user=session["users"][username], channel_list=channel_list)
    if request.method == "POST":
        if session.get('user') and session.get('user_name'):
            
            session["channel_name"] = channel_name
            username = session.get('user_name')
            channel_list = session["users"][username]["channel_list"]
            
            message = request.form.get('message')
            new_msg = {"username": session["user_name"], "date": time, "message": message, "image": session["users"][username]['image'] }
            session["channel_messages"][channel_name].append(new_msg)
            
            all_messages = session["channel_message"][channel_name]
            return render_template("profile.html", messages=all_messages, username=session["user_name"], user=session["users"][username], channel_list=channel_list), jsonify({"success": True, "new_msg": new_msg, "all_msgs":all_messages})
                
        
@socketio.on("send message")
def message(data):
    username = session.get('user_name')
    channel_name = session.get("channel_name")

    new_msg = {"username": session["user_name"], "date": time, "message": data['new_msg'], "image": session["users"][username]['image'] }
    session["channel_messages"][channel_name].append(new_msg)
            
    emit("show message", {**new_msg}, broadcast=True)z
                
        

@app.route("/logout")
def logout():
    session['user_name'] = ""
    session["channel_name"] = ""

    return redirect("/")

if __name__ == "__main__":
    socketio.run(app)
    app.run()

