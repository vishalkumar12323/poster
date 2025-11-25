from flask import Flask, render_template, request, session, redirect, url_for
from controllers.user_controllers import login_user, register_user
from lib.connection import client, User, Post
from sqlalchemy.orm import defer
from typing import Any, cast
from sqlalchemy.orm.attributes import QueryableAttribute
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    if session.get("is_logged_in"):
        user_id = session.get("user_id")
        logged_in_user = client.query(User).filter_by(id=user_id).options(defer(cast(QueryableAttribute[Any], User.password))).first()

        if logged_in_user:
            posts = client.query(Post).filter_by(user_id=user_id).all()
            
            return render_template('index.html', user=logged_in_user, posts=posts, is_logged_in=session.get("is_logged_in"))
        
    return redirect(url_for("login"), code=302)


@app.route("/dashboard")
def dashboard():
    return ""


@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        return {"error": "Email and password are required"}, 400
    
    return login_user(user={"email": email, "password": password})


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "GET":
        return render_template("register.html")
    
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if name is None or email is None or password is None:
        return "<h2>Name, Email or Password is required feild.</h2>"

    return register_user(user={"name": name, "email": email, "password": password})
    


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)