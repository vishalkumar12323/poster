from flask import Flask, render_template
from flask_login import (
    LoginManager,
    login_required, current_user
)
import os
from lib.models import db, User, Post
from controllers.user_controllers import register, login, logout
from controllers.post_controllers import view, create, edit, delete
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app=app)
# use setattr to avoid static type checker assignment error
setattr(login_manager, "login_view", "login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html", user=current_user)

@app.route("/dashboard")
@login_required
def dashboard():
    user_posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, posts=user_posts)


@app.route("/register", methods=["GET", "POST"])
def signup():
    return register()

@app.route("/login", methods=["GET", "POST"])
def signin():
    return login()


@app.route("/logout")
@login_required
def logout_user():
    return logout()



@app.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():
    return create()


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    return edit(post_id)



@app.route("/delete-post/<int:post_id>", methods=["POST", "GET"])
@login_required
def delete_post(post_id):
    return delete(post_id)


@app.route("/view-post/<int:post_id>")
@login_required
def view_post(post_id):
    return view(post_id)


if __name__ == "__main__":
    if not os.path.exists("instance/poster.db"):
        with app.app_context():
            db.create_all()
    
    app.run(debug=True)