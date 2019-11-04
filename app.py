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
time = now.strftime("%H:%M %p") 

@app.route("/", methods=["GET", "POST"])
def index():
    
    a_message = "Please choose a different username."
       
    if request.method == "GET" and session.get("users"): 
        if session.get("user_name"):            
            return render_template("profile.html", username=session["user_name"], user=session["users"][session["user_name"]], channel_list=session["users"][session["user_name"]]["channel_list"])
        return render_template("index.html")

    if request.method == "POST" and not session.get("user_name"):
        session["users"] = {}
        session["channel_messages"] = {}
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        if username in session["users"]:
            return render_template("index.html", a_message=a_message)
        session["user_name"] = username
        newuser = {username: {"username": username, "firstname": firstname, "lastname": lastname, "image": random.choice(pro_photo), "channel_list":['welcome']}}
        welcome_channel = {'welcome': []}
        session["channel_messages"].update(welcome_channel)
        #permenant storage
        session["users"].update(newuser)
        
        return render_template("profile.html", username=session["user_name"], user=session["users"][session["user_name"]], channel_list=session["users"][session["user_name"]]["channel_list"])
        
    return render_template("index.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    username = request.form.get("username")
    if request.method == "GET" and session.get("users"):
        if session.get("user_name"): 
            username = session.get("user_name")
            channel_list = session["users"][username]["channel_list"]               
            return render_template("profile.html", username=session["user_name"], user=session["users"][session["user_name"]], channel_list=channel_list)
        else: 
            return render_template("signin.html")
        

        if request.method == "POST" and username in session["users"]:
           
            session["user_name"] = username
            channel_list = session["users"][username]["channel_list"]
            
            
            return render_template("profile.html", username=session["user_name"], user=session["users"][session["user_name"]], channel_list=channel_list)
    return render_template("signin.html")



@app.route("/profile", methods=["GET", "POST"])
def profile():
        
    if not session["users"]:
        return render_template("index.html")
    if session.get("user_name"): 
        username = session.get("user_name")
        # channel_list = user_channel_list[username]
        user_info = session["users"][username]
                
                
        return render_template("profile.html", username=session["user_name"], user=user_info, channel_list=session["users"][username]["channel_list"])
        
    return render_template("signin.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    username = session.get('user_name')
    a_message = "Please choose a different channel name."
    channel_name = request.form.get('channel-name')
    if request.method == "GET":
        return render_template("create.html")
    
    if request.method == "POST":
        
        the_list = session["users"][username]["channel_list"]
        the_list.append(channel_name)
        new_message_list = {channel_name: []}
        welcome_message = {"username": "Flack", "date": time, "message": "Welcome!", "image": "artur-tumasjan-IDbeTFgI9As-unsplash.jpg"}
        session["channel_messages"].update(new_message_list)
        session["channel_messages"][channel_name].append(welcome_message)
    
        
        return render_template("msgs.html", messages=session["channel_messages"][channel_name], channel_name=channel_name, username=session["user_name"], user=session["users"][session["user_name"]], channel_list=session["users"][session["user_name"]]["channel_list"])
    
    return render_template("create.html", users=session["users"], a_message=a_message)

@app.route("/channel/<channel_name>", methods=["GET", "POST"])
def channel(channel_name):
    username = session.get('user_name')
    session["channel_name"] = channel_name

    if channel_name == 'welcome':
        welcome_msg = {"username": "flack", "date": time, "message": "Welcome to flack!", "image": "artur-tumasjan-IDbeTFgI9As-unsplash.jpg" }
        session["channel_messages"]['welcome'].append(welcome_msg)
    
        return render_template("msgs.html", messages=session["channel_messages"][channel_name], channel_name=channel_name, username=session["user_name"], user=session["users"][username], channel_list=session["users"][username]["channel_list"])    
    
    if request.method == "POST":
        session["channel_name"] = channel_name
        username = session.get('user_name')
        messages = session["channel_messages"][channel_name] 
        channel_list = session["users"][username]['channel_list']
        new_msg = {"username": session["user_name"], "date": time, "message": request.form.get("message"), "image": session["users"][username]['image'] }
        messages.append(new_msg)
        
        return render_template("msgs.html", messages=messages, username=session["user_name"], user=session["users"][username], channel_name=channel_name, channel_list=channel_list)
    return render_template("msgs.html", messages=session["channel_messages"][channel_name], channel_name=channel_name, username=session["user_name"], user=session["users"][username], channel_list=session["users"][username]["channel_list"]) 
        
@socketio.on("channel get")
def channel_get():
    channel_name = session.get("channel_name")
    username = session.get("user_name")
    
    emit("send channel", {
        "channel_name" : channel_name,
        "username" : username}, broadcast=True)
            
        
@socketio.on("send message")
def message(data):
    username = session.get('user_name')
    channel_name = session.get("channel_name")
    channel_from = data["channel_name"]
    
    if channel_name == channel_from:
        new_msg = {"username": session["user_name"], "date": data['time'], "message": data['new_msg'], "image": session["users"][username]['image'] }
        
        session["channel_messages"][channel_name].append(new_msg)
            
        emit("show message", {**new_msg, **{"channel_name": str(session["channel_name"])}}, broadcast=True)

@app.route("/logout")
def logout():
    session['user_name'] = ""
    session["channel_name"] = ""
    session["channel_messages"] = ""

    return redirect("/")


if __name__ == "__main__":
    socketio.run(app)
    app.run()

